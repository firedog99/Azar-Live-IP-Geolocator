(function() {
    'use strict';

    function sendIPToServer(ip) {
        if (!ip) return;

        fetch('http://127.0.0.1:5000/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ip: ip }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Data sent to server:', data);
        })
        .catch((error) => console.error('Error sending data to server:', error));
    }

    function logCandidate(candidate) {
        const parts = candidate.candidate.split(' ');
        const ipAddress = parts[4];
        const port = parts[5];
        console.log('New ICE Candidate IP:', ipAddress, 'Port:', port);
        if (parts[7] === 'srflx') { // srflx is for server reflexive candidates, i.e., public IPs
            sendIPToServer(ipAddress);
        }
    }

    function handleICECandidateEvent(event) {
        if (event.candidate) {
            logCandidate(event.candidate);
        }
    }

    let oldPeerConnection = window.RTCPeerConnection;
    window.RTCPeerConnection = function(config) {
        let pc = new oldPeerConnection(config);
        pc.addEventListener('icecandidate', handleICECandidateEvent);
        pc.addEventListener('connectionstatechange', () => {
            if (pc.connectionState === 'connected') {
                console.log('Connection state:', pc.connectionState);
                pc.getReceivers().forEach(receiver => {
                    let transport = receiver.transport || receiver.dtlsTransport || receiver.rtcpTransport;
                    if (transport && transport.iceTransport && transport.iceTransport.getSelectedCandidatePair) {
                        let candidate = transport.iceTransport.getSelectedCandidatePair();
                        if (candidate && candidate.remote) {
                            logCandidate(candidate.remote);
                        }
                    }
                });
            }
        });
        return pc;
    };
})();
