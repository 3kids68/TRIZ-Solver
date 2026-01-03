const state = {
    improvingParam: null,
    worseningParam: null
};

function validateAndNext(currentStep) {
    if (currentStep === 1) {
        const name = document.getElementById('sys-name').value;
        if (name.length < 3) {
            alert("Please enter a valid system name to proceed.");
            return;
        }
        goToStep(2);
    }
}

function log(msg) {
    const consoleEl = document.getElementById('log-content');
    const line = document.createElement('span');
    line.className = 'log-line';
    line.innerText = `> ${msg}`;
    consoleEl.appendChild(line);
    consoleEl.scrollTop = consoleEl.scrollHeight;
}

function goToStep(num) {
    document.querySelectorAll('.wizard-step').forEach(el => el.classList.remove('active'));
    document.getElementById(`step-${num}`).classList.add('active');

    document.querySelectorAll('.step').forEach(el => el.classList.remove('active'));
    document.getElementById(`step${num}-indicator`).classList.add('active');

    log(`Navigate to Step ${num}`);
}

async function analyzeInput(type) {
    const inputEl = document.getElementById(`input-${type}`);
    const text = inputEl.value;

    if (!text) {
        log(`Error: Empty input for ${type}`);
        return;
    }

    log(`Analyzing ${type} input: "${text}"...`);

    // UI Loading state
    inputEl.disabled = true;

    try {
        const response = await fetch('/api/normalize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        // Print Internal AI Logs (Transparency)
        data.logs.forEach(l => log(`[AI] ${l}`));

        if (data.match) {
            const param = data.match;
            // Update State
            if (type === 'improving') state.improvingParam = param;
            if (type === 'worsening') state.worseningParam = param;

            // Show UI
            document.getElementById(`res-${type}-name`).innerText = param.name;
            document.getElementById(`res-${type}-id`).innerText = `ID: ${param.id}`;
            document.getElementById(`suggestion-${type}`).style.display = 'flex';

            checkReadyToSolve();
        } else {
            log(`[Warning] No high-confidence match for input.`);
            alert("AI could not confidently identify the parameter. Please try specific keywords like 'Weight' or 'Speed'.");
        }
    } catch (e) {
        log(`Error reaching API: ${e}`);
    } finally {
        inputEl.disabled = false;
    }
}

function checkReadyToSolve() {
    const btn = document.getElementById('btn-solve');
    if (state.improvingParam && state.worseningParam) {
        btn.disabled = false;
        log('Ready to solve contradiction.');
    }
}

async function solveContradiction() {
    goToStep(3);
    log('Initiating Matrix Lookup...');

    const container = document.getElementById('principles-container');
    container.innerHTML = '<div style="color:white">Calculating...</div>';

    try {
        const response = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                improving_id: state.improvingParam.id,
                worsening_id: state.worseningParam.id
            })
        });

        const report = await response.json();

        // Log Logic
        report.execution_log.forEach(l => log(`[Engine] ${l}`));

        document.getElementById('strategy-display').innerText = report.strategy_note;

        // Render Principles
        container.innerHTML = '';
        report.suggested_principles.forEach(p => {
            const card = document.createElement('div');
            card.className = 'principle-card';
            card.innerHTML = `
                <div class="principle-header">
                    <span class="p-name">${p.name}</span>
                    <span class="p-id">#${p.id}</span>
                </div>
                <div class="p-desc">${p.description}</div>
                <div class="p-examples">Ex: ${p.examples.join(', ')}</div>
            `;
            container.appendChild(card);
        });

    } catch (e) {
        log(`Error solving: ${e}`);
        container.innerHTML = 'Error generating solution.';
    }
}

function restart() {
    state.improvingParam = null;
    state.worseningParam = null;
    document.getElementById('input-improving').value = '';
    document.getElementById('input-worsening').value = '';
    document.getElementById('suggestion-improving').style.display = 'none';
    document.getElementById('suggestion-worsening').style.display = 'none';
    document.getElementById('btn-solve').disabled = true;
    goToStep(1);
    log('System Reset.');
}
