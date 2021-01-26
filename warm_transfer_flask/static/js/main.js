(function () {
    let currentAgentId;
    const callStatus = document.getElementById('call-status');
    const connectAgent1Button = document.getElementById("connect-agent1-button");
    const connectAgent2Button = document.getElementById("connect-agent2-button");

    const answerCallButton = document.getElementById("answer-call-button");
    const hangupCallButton = document.getElementById("hangup-call-button");
    const dialAgent2Button = document.getElementById("dial-agent2-button");

    const connectAgentRow = document.getElementById('connect-agent-row');
    const connectedAgentRow = document.getElementById('connected-agent-row');

    connectAgent1Button.onclick = () => { connectAgent('agent1') };
    connectAgent2Button.onclick = () => { connectAgent('agent2') };
    dialAgent2Button.onclick = dialAgent2;

    const device = new Twilio.Device();

    device.on('ready', function (device) {
        callStatus.innerText = "Ready";
        connectAgent1Button.classList.add('hidden');
        connectAgent2Button.classList.add('hidden');
        agentConnectedHandler(currentAgentId);
    });

    device.on('offline', function (device) {
        callStatus.innerText = "Offline";
        connectAgent1Button.disabled = false;
        connectAgent2Button.disabled = false;
        connectedAgentRow.classList.add('hidden');
        connectAgentRow.classList.remove('hidden');
    });

    // Callback for when Twilio Client receives a new incoming call
    device.on('incoming', function (connection) {
        callStatus.innerText = "Incoming support call";

        // Set a callback to be executed when the connection is accepted
        connection.accept(function () {
            callStatus.innerText = "In call with customer";
            answerCallButton.disabled = true;
            hangupCallButton.disabled = false;
            dialAgent2Button.disabled = false;
        });

        // Set a callback on the answer button and enable it
        answerCallButton.onclick = () => {
            connection.accept();
        };
        answerCallButton.disabled = false;
    });

    /* Report any errors to the call status display */
    device.on('error', function (error) {
        callStatus.innerText = `ERROR: ${error.message}`;
        connectAgent1Button.disabled = false;
        connectAgent2Button.disabled = false;
    });

    // Callback for when the call finalizes
    device.on('disconnect', function (connection) {
        dialAgent2Button.disabled = true;
        hangupCallButton.disabled = true;
        answerCallButton.disabled = true;
        callStatus.innerText = `Connected as: ${currentAgentId}`;
    });

    hangupCallButton.onclick = () => { device.disconnectAll() };

    function connectAgent(agentId) {
        connectAgent1Button.disabled = true;
        connectAgent2Button.disabled = true;
        currentAgentId = agentId;
        fetch('/' + agentId + '/token', { method: 'POST' })
            .then(response => response.json())
            .then(function (data) {
                device.setup(data.token);
            })
            .catch(error => {
                callStatus.innerText = `ERROR: ${error.message}`;
            });
    }

    function dialAgent2() {
        fetch('/conference/' + currentAgentId + '/call', { method: 'POST' });
    }

    function agentConnectedHandler(agentId) {
        connectAgentRow.classList.add('hidden');
        connectedAgentRow.classList.remove('hidden');
        callStatus.innerText = `Connected as: ${agentId}`;

        if (agentId === 'agent1') {
            dialAgent2Button.classList.remove('hidden');
            dialAgent2Button.attributes.disabled = true;
        } else {
            dialAgent2Button.classList.add('hidden');
        }
    }

})();
