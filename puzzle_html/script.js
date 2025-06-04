document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const mainMenu = document.getElementById('main-menu');
    const gameScreen = document.getElementById('game-screen');
    const gameOver = document.getElementById('game-over');
    const startButton = document.getElementById('start-button');
    const exitButton = document.getElementById('exit-button');
    const backButton = document.getElementById('back-button');
    const retryButton = document.getElementById('retry-button');
    const menuButton = document.getElementById('menu-button');
    const timeDisplay = document.getElementById('time');
    const scoreDisplay = document.getElementById('score');
    const sumDisplay = document.getElementById('sum');
    const finalScoreDisplay = document.getElementById('final-score');
    const panelsContainer = document.getElementById('panels-container');

    // Game variables
    let gameTimer;
    let score = 0;
    let selectedPanels = [];
    let currentSum = 0;
    let panels = [];
    let gameActive = false;

    // Event listeners for buttons
    startButton.addEventListener('click', startGame);
    exitButton.addEventListener('click', exitGame);
    backButton.addEventListener('click', returnToMenu);
    retryButton.addEventListener('click', startGame);
    menuButton.addEventListener('click', returnToMenu);

    // Initialize the game
    function startGame() {
        // Reset game state
        score = 0;
        selectedPanels = [];
        currentSum = 0;
        panels = [];
        gameActive = true;
        
        // Update displays
        scoreDisplay.textContent = score;
        sumDisplay.textContent = '0';
        timeDisplay.textContent = '60';
        
        // Show game screen
        mainMenu.classList.add('hidden');
        gameOver.classList.add('hidden');
        gameScreen.classList.remove('hidden');
        
        // Create panels
        createPanels();
        
        // Start game timer
        startGameTimer();
    }

    // Create the 9 panels with random numbers
    function createPanels() {
        panelsContainer.innerHTML = '';
        panels = [];
        
        for (let i = 0; i < 9; i++) {
            const panel = createPanel();
            panelsContainer.appendChild(panel.element);
            panels.push(panel);
        }
    }

    // Create a single panel
    function createPanel() {
        const number = Math.floor(Math.random() * 9) + 1;
        const panelElement = document.createElement('div');
        panelElement.className = 'panel';
        panelElement.textContent = number;
        
        // Create timer bar
        const timerBar = document.createElement('div');
        timerBar.className = 'timer-bar';
        panelElement.appendChild(timerBar);
        
        // Panel object
        const panel = {
            element: panelElement,
            number: number,
            selected: false,
            timerBar: timerBar,
            resetTimer: null
        };
        
        // Add click event
        panelElement.addEventListener('click', () => {
            if (!gameActive) return;
            togglePanelSelection(panel);
        });
        
        // Start panel reset timer
        startPanelResetTimer(panel);
        
        return panel;
    }

    // Toggle panel selection
    function togglePanelSelection(panel) {
        if (panel.selected) {
            // Deselect panel
            panel.selected = false;
            panel.element.classList.remove('selected');
            
            // Remove from selected panels
            const index = selectedPanels.indexOf(panel);
            if (index !== -1) {
                selectedPanels.splice(index, 1);
                currentSum -= panel.number;
            }
        } else {
            // Select panel
            panel.selected = true;
            panel.element.classList.add('selected');
            selectedPanels.push(panel);
            currentSum += panel.number;
        }
        
        // Update sum display
        sumDisplay.textContent = `${currentSum}/15`;
        
        // Check if sum is 15
        if (currentSum === 15 && selectedPanels.length >= 2) {
            handleSumFifteen();
        } else if (currentSum > 15) {
            // Optional: provide visual feedback that sum is too high
            sumDisplay.style.color = 'red';
            setTimeout(() => {
                sumDisplay.style.color = '';
            }, 500);
        }
    }

    // Handle when sum equals 15
    function handleSumFifteen() {
        // Add points
        score += 15;
        scoreDisplay.textContent = score;
        
        // Replace selected panels with new ones
        selectedPanels.forEach(panel => {
            // Clear the panel's reset timer
            clearTimeout(panel.resetTimer);
            
            // Get panel index
            const index = panels.indexOf(panel);
            if (index !== -1) {
                // Create new panel
                const newPanel = createPanel();
                
                // Replace old panel with new one
                panelsContainer.replaceChild(newPanel.element, panel.element);
                panels[index] = newPanel;
            }
        });
        
        // Reset selection
        selectedPanels = [];
        currentSum = 0;
        sumDisplay.textContent = '0/15';
    }

    // Start panel reset timer (15 seconds)
    function startPanelResetTimer(panel) {
        // Animate timer bar
        panel.timerBar.style.transition = 'transform 15s linear';
        panel.timerBar.style.transform = 'scaleX(0)';
        
        // Set timeout to reset panel after 15 seconds
        panel.resetTimer = setTimeout(() => {
            if (!gameActive) return;
            
            // Deduct points if panel is reset
            score -= 10;
            scoreDisplay.textContent = score;
            
            // Check if panel is selected
            if (panel.selected) {
                // Remove from selected panels
                const index = selectedPanels.indexOf(panel);
                if (index !== -1) {
                    selectedPanels.splice(index, 1);
                    currentSum -= panel.number;
                    sumDisplay.textContent = `${currentSum}/15`;
                }
            }
            
            // Create new panel
            const newPanel = createPanel();
            
            // Replace old panel with new one
            const panelIndex = panels.indexOf(panel);
            if (panelIndex !== -1) {
                panelsContainer.replaceChild(newPanel.element, panel.element);
                panels[panelIndex] = newPanel;
            }
        }, 15000);
    }

    // Start game timer (60 seconds)
    function startGameTimer() {
        let timeLeft = 60;
        
        gameTimer = setInterval(() => {
            timeLeft--;
            timeDisplay.textContent = timeLeft;
            
            if (timeLeft <= 0) {
                endGame();
            }
        }, 1000);
    }

    // End the game
    function endGame() {
        gameActive = false;
        clearInterval(gameTimer);
        
        // Clear all panel timers
        panels.forEach(panel => {
            clearTimeout(panel.resetTimer);
        });
        
        // Show game over screen
        gameScreen.classList.add('hidden');
        gameOver.classList.remove('hidden');
        finalScoreDisplay.textContent = score;
    }

    // Return to main menu
    function returnToMenu() {
        gameActive = false;
        clearInterval(gameTimer);
        
        // Clear all panel timers
        panels.forEach(panel => {
            clearTimeout(panel.resetTimer);
        });
        
        gameScreen.classList.add('hidden');
        gameOver.classList.add('hidden');
        mainMenu.classList.remove('hidden');
    }

    // Exit game
    function exitGame() {
        // In a browser context, we can't truly "exit" the application
        // So we'll just show a message
        alert('ゲームを終了します。ブラウザタブを閉じてください。');
    }
});
