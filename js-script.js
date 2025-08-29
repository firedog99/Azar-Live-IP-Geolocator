(function() {
    'use strict';
    function sendIPToServer(ip) {
        if (!ip) return;
        fetch('http://127.0.0.1:5000/data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ip: ip }),
        })
        .then(response => response.json())
        .then(data => console.log('Data sent to server:', data))
        .catch(error => console.error('Error sending data to server:', error));
    }

    function logCandidate(candidate) {
        if (!candidate || !candidate.candidate) return;
        const parts = candidate.candidate.split(' ');
        const ipAddress = parts[4];
        if (parts[7] === 'srflx') { // Only send public IPs
            sendIPToServer(ipAddress);
        }
    }

    function handleICECandidateEvent(event) {
        if (event.candidate) logCandidate(event.candidate);
    }

    const OldRTCPeerConnection = window.RTCPeerConnection;
    window.RTCPeerConnection = function(config) {
        const pc = new OldRTCPeerConnection(config);
        pc.addEventListener('icecandidate', handleICECandidateEvent);
        return pc;
    };
})();
