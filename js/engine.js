/**
 * TRIZ Engine - Pure JavaScript Implementation
 * Ported from Python engine.py for GitHub Pages deployment
 */

class TRIZEngine {
    constructor() {
        this.parameters = {};
        this.principles = {};
        this.matrix = {};
        this.dataLoaded = false;
    }

    /**
     * Load all TRIZ data from JSON files
     */
    async loadData() {
        try {
            // Load Parameters
            const paramsResponse = await fetch('data/parameters.json');
            const paramsData = await paramsResponse.json();
            paramsData.forEach(p => {
                this.parameters[p.id] = p;
            });

            // Load Principles
            const principlesResponse = await fetch('data/principles.json');
            const principlesData = await principlesResponse.json();
            principlesData.forEach(p => {
                this.principles[p.id] = p;
            });

            // Load Matrix
            const matrixResponse = await fetch('data/matrix.json');
            this.matrix = await matrixResponse.json();

            this.dataLoaded = true;
            console.log('[Engine] Data loaded successfully');
            console.log(`[Engine] ${Object.keys(this.parameters).length} parameters`);
            console.log(`[Engine] ${Object.keys(this.principles).length} principles`);
            console.log(`[Engine] ${Object.keys(this.matrix).length} matrix cells`);
        } catch (error) {
            console.error('[Engine] Error loading data:', error);
            throw new Error('Failed to load TRIZ data');
        }
    }

    /**
     * Normalize user input to engineering parameter
     * @param {string} userText - User's natural language input
     * @returns {Object} { match: Parameter|null, logs: string[] }
     */
    normalizeInputToParameter(userText) {
        const logs = [];
        userText = userText.toLowerCase();
        
        logs.push(`Analyzing input: '${userText}'`);

        let bestMatch = null;
        let maxScore = 0;
        const candidates = [];

        // Score each parameter based on keyword matching
        for (const param of Object.values(this.parameters)) {
            let score = 0;
            const matchedKws = [];

            for (const kw of param.keywords) {
                // Simple substring match
                if (userText.includes(kw.toLowerCase())) {
                    score += 1;
                    matchedKws.push(kw);
                }
            }

            if (score > 0) {
                candidates.push({ param, score, matchedKws });
                if (score > maxScore) {
                    maxScore = score;
                    bestMatch = param;
                }
            }
        }

        // Sort candidates by score
        candidates.sort((a, b) => b.score - a.score);

        if (candidates.length > 0) {
            const top3 = candidates.slice(0, 3);
            logs.push(`Found ${candidates.length} potential candidates.`);
            top3.forEach(c => {
                logs.push(` - Candidate [${c.param.id}] '${c.param.name}': Score ${c.score} (Keywords: ${c.matchedKws.join(', ')})`);
            });
        } else {
            logs.push('No keywords matched.');
        }

        if (bestMatch) {
            logs.push(`Primary match selected: ID ${bestMatch.id}`);
        }

        return { match: bestMatch, logs };
    }

    /**
     * Solve technical contradiction using TRIZ matrix
     * @param {number} improvingId - ID of improving parameter
     * @param {number} worseningId - ID of worsening parameter
     * @returns {Object} Solution report
     */
    solveContradiction(improvingId, worseningId) {
        const logs = [];
        logs.push('Initiating TRIZ Logic Block: Matrix Lookup');

        const improving = this.parameters[improvingId];
        const worsening = this.parameters[worseningId];

        if (!improving || !worsening) {
            throw new Error('Invalid Parameter IDs');
        }

        logs.push(`Improving Parameter: [${improvingId}] ${improving.name}`);
        logs.push(`Worsening Parameter: [${worseningId}] ${worsening.name}`);

        // Check for Physical Contradiction (A vs A)
        if (improvingId === worseningId) {
            logs.push('!! PHYSICAL CONTRADICTION DETECTED !! (A vs A)');
            logs.push('Switching logic to SEPARATION PRINCIPLES.');
            
            const separationPrinciples = [
                {
                    id: 999,
                    name: 'Separation in Time (時間分離)',
                    description: 'Separate conflicting properties in time. (在時間上分離矛盾特性)',
                    examples: ['Traffic lights separate flow', 'Day/night operations']
                },
                {
                    id: 998,
                    name: 'Separation in Space (空間分離)',
                    description: 'Separate conflicting properties in space. (在空間上分離矛盾特性)',
                    examples: ['Bicycle path vs Car lane', 'Zoning in buildings']
                },
                {
                    id: 997,
                    name: 'Separation by Condition (條件分離)',
                    description: 'Separate conflicting properties by changing conditions. (透過改變條件分離矛盾特性)',
                    examples: ['Temperature-sensitive materials', 'Adaptive structures']
                }
            ];

            return {
                improving_parameter: improving,
                worsening_parameter: worsening,
                suggested_principles: separationPrinciples,
                strategy_note: 'PHYSICAL CONTRADICTION (物理矛盾)',
                execution_log: logs
            };
        }

        // Lookup Matrix
        const key = `${improvingId},${worseningId}`;
        logs.push(`Querying Matrix Cell [${improvingId}, ${worseningId}]...`);
        
        let principleIds = this.matrix[key] || [];
        let note = '';
        const suggested = [];

        if (principleIds.length === 0) {
            logs.push('Matrix Cell is EMPTY (No classic recommendation).');
            logs.push('Applying HEURISTIC FALLBACK (Top 4 general principles).');
            principleIds = [35, 10, 1, 28]; // Universal principles
            note = 'Heuristic Fallback (啟發式建議 - 矩陣無直接對應)';
        } else {
            logs.push(`Matrix Match Found! Principles: ${principleIds.join(', ')}`);
            note = 'Standard Matrix Solution (標準矩陣解)';
        }

        // Fetch principle details
        for (const pid of principleIds) {
            const principle = this.principles[pid];
            if (principle) {
                suggested.push(principle);
            } else {
                logs.push(`Warning: Principle ID ${pid} not found in database.`);
            }
        }

        return {
            improving_parameter: improving,
            worsening_parameter: worsening,
            suggested_principles: suggested,
            strategy_note: note,
            execution_log: logs
        };
    }
}

// Export for use in main.js
window.TRIZEngine = TRIZEngine;
