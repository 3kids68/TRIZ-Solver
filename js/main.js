// Global state
const state = {
    improvingParam: null,
    worseningParam: null,
    engine: null
};

// Initialize engine on page load
window.addEventListener('DOMContentLoaded', async () => {
    log('Initializing TRIZ Engine...');
    state.engine = new TRIZEngine();

    try {
        await state.engine.loadData();
        log('✓ Engine ready. All data loaded.');
    } catch (error) {
        log(`✗ Failed to load engine: ${error.message}`);
        alert('Failed to load TRIZ data. Please refresh the page.');
    }
});

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
    if (!state.engine || !state.engine.dataLoaded) {
        alert('Engine is not ready yet. Please wait a moment.');
        return;
    }

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
        // Use local engine instead of API
        const result = state.engine.normalizeInputToParameter(text);

        // Print Internal AI Logs (Transparency)
        result.logs.forEach(l => log(`[AI] ${l}`));

        if (result.match) {
            const param = result.match;
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
        log(`Error analyzing input: ${e.message}`);
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
    if (!state.engine || !state.engine.dataLoaded) {
        alert('Engine is not ready yet.');
        return;
    }

    goToStep(3);
    log('Initiating Matrix Lookup...');

    const container = document.getElementById('principles-container');
    container.innerHTML = '<div style="color:white">Calculating...</div>';

    try {
        // Use local engine instead of API
        const report = state.engine.solveContradiction(
            state.improvingParam.id,
            state.worseningParam.id
        );

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
        log(`Error solving: ${e.message}`);
        container.innerHTML = '<div style="color:white">Error generating solution.</div>';
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

// Help Modal Functions
function openHelpModal() {
    const modal = document.getElementById('help-modal');
    modal.classList.add('active');
    // Close when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeHelpModal();
        }
    });
}

function closeHelpModal() {
    document.getElementById('help-modal').classList.remove('active');
}
