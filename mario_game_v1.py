"""
Super Mario Obstacle Game
- Control Mario with arrow keys (← →) to move and (↑) to jump
- Jump over obstacles (brown boxes)
- Evade incoming mushrooms from sides
- Hitting a mushroom ends the game and restarts
- Avoid obstacles by jumping
- No life limit - game restarts instantly on collision

NO EXTERNAL DEPENDENCIES - Uses built-in Python modules only!
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from urllib.parse import urlparse

# HTML Template with embedded CSS and JavaScript
GAME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super Mario Obstacle Game</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .container {
            text-align: center;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }

        .info {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: left;
        }

        .info h3 {
            color: #667eea;
            margin-bottom: 10px;
        }

        .info p {
            margin: 8px 0;
            color: #555;
            font-size: 0.95em;
        }

        .info strong {
            color: #333;
        }

        #gameContainer {
            position: relative;
            width: 800px;
            height: 400px;
            background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 100%);
            border: 3px solid #333;
            border-radius: 10px;
            overflow: hidden;
            margin: 20px auto;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            outline: none;
        }

        .ground {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 60px;
            background: linear-gradient(to bottom, #8B7355 0%, #654321 100%);
            border-top: 3px dashed #333;
        }

        .mario {
            position: absolute;
            bottom: 60px;
            left: 50px;
            width: 40px;
            height: 50px;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 50"><rect fill="%23FF0000" width="40" height="30"/><circle cx="10" cy="10" r="5" fill="%23FFD700"/><circle cx="30" cy="10" r="5" fill="%23FFD700"/><circle cx="20" cy="20" r="3" fill="%23000"/><rect fill="%23FF0000" y="30" width="12" height="20"/><rect fill="%23FF0000" x="28" y="30" width="12" height="20"/></svg>') no-repeat center;
            background-size: contain;
            z-index: 10;
        }

        .obstacle {
            position: absolute;
            bottom: 60px;
            width: 30px;
            height: 50px;
            background: #8B6914;
            border: 2px solid #654321;
            border-radius: 3px;
        }

        .mushroom {
            position: absolute;
            bottom: 60px;
            width: 35px;
            height: 35px;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 35 35"><circle cx="17.5" cy="12" r="12" fill="%23FF0000"/><rect fill="%23FFCC00" x="12" y="20" width="11" height="15"/></svg>') no-repeat center;
            background-size: contain;
            border-radius: 50%;
        }

        .gameOver {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            z-index: 100;
            display: none;
            min-width: 300px;
        }

        .gameOver h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
        }

        .gameOver p {
            font-size: 1.2em;
            margin: 15px 0;
        }

        .gameOver.show {
            display: block;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 10px;
            font-size: 1.1em;
        }

        .stats div {
            flex: 1;
        }

        .stats strong {
            color: #667eea;
            font-size: 1.3em;
        }

        #debugLog {
            background: #222;
            color: #0f0;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.85em;
            max-height: 120px;
            overflow-y: auto;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        #keyDisplay {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 255, 255, 0.8);
            padding: 5px 10px;
            border-radius: 3px;
            font-weight: bold;
            color: #333;
            z-index: 50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍄 Super Mario Obstacle Game 🍄</h1>
        
        <div class="info">
            <h3>How to Play:</h3>
            <p><strong>Controls:</strong> Use ← → Arrow Keys to move, SPACEBAR to jump</p>
            <p><strong>Objective:</strong> Jump over brown obstacles and avoid incoming mushrooms</p>
            <p><strong>Rules:</strong></p>
            <ul style="margin-left: 20px;">
                <li>Colliding with a mushroom 🍄 kills Mario (game restarts)</li>
                <li>Land on obstacles to avoid them - don't collide</li>
                <li>Unlimited lives - instantly restart on collision</li>
                <li>Try to get the highest score!</li>
            </ul>
        </div>

        <div id="gameContainer">
            <div id="keyDisplay">Last Key: -</div>
            <div class="mario" id="mario"></div>
            <div class="gameOver" id="gameOverScreen">
                <h2>GAME OVER!</h2>
                <p>Mario Died! 💀</p>
                <p id="finalScore">Score: 0</p>
                <p style="margin-top: 20px; font-size: 0.9em;">Game restarts automatically...</p>
            </div>
            <div class="ground"></div>
        </div>

        <div class="stats">
            <div>⏱️ Time: <strong id="timer">0</strong>s</div>
            <div>📊 Score: <strong id="score">0</strong></div>
            <div>🎮 Status: <strong id="status">Playing</strong></div>
        </div>

        <button id="jumpBtn" style="margin-top: 15px; padding: 10px 20px; font-size: 1.1em; cursor: pointer; background: #667eea; color: white; border: none; border-radius: 5px;">Jump Test Button</button>

        <div id="debugLog">Debug: Ready to receive input...</div>
    </div>

    <script>
        // Game Constants
        const GROUND_HEIGHT = 60;
        const GRAVITY = 0.8;  // Twice as strong gravity
        const JUMP_POWER = 18;
        const MARIO_START_X = 50;
        const CONTAINER_WIDTH = 800;
        const CONTAINER_HEIGHT = 400;

        // Game State
        let mario = {
            x: MARIO_START_X,
            y: CONTAINER_HEIGHT - GROUND_HEIGHT - 50,
            velocityY: 0,
            width: 40,
            height: 50,
            isJumping: false
        };

        let gameState = {
            score: 0,
            time: 0,
            isGameActive: true,
            gameOverTime: 0
        };

        let keys = { left: false, right: false, space: false };
        let obstacles = [];
        let mushrooms = [];
        let canJump = true;
        let lastSpaceState = false;  // Track previous space state to detect new presses

        // DOM Elements
        const gameContainer = document.getElementById('gameContainer');
        const marioElement = document.getElementById('mario');
        const gameOverScreen = document.getElementById('gameOverScreen');
        const scoreDisplay = document.getElementById('score');
        const timerDisplay = document.getElementById('timer');
        const statusDisplay = document.getElementById('status');
        const finalScoreDisplay = document.getElementById('finalScore');
        const debugLog = document.getElementById('debugLog');
        const keyDisplay = document.getElementById('keyDisplay');

        // Debug helper
        let debugMessages = [];
        function addDebug(msg) {
            debugMessages.unshift(msg);
            if (debugMessages.length > 3) debugMessages.pop();
            debugLog.textContent = 'Debug: ' + debugMessages.join(' | ');
            console.log('DEBUG: ' + msg);
        }

        addDebug('Game initialized');

        // Debug: Show initial Mario position
        console.log('Initial mario.y:', mario.y);
        console.log('Initial velocityY:', mario.velocityY);
        console.log('Ground level (mario.y + height should be >= CONTAINER_HEIGHT - GROUND_HEIGHT):',
                    CONTAINER_HEIGHT - GROUND_HEIGHT);
        console.log('Mario bounds:', mario.y, mario.y + mario.height, 'should touch', CONTAINER_HEIGHT - GROUND_HEIGHT);
        addDebug(`Initial: Mario Y=${Math.round(mario.y)}, Vel=${mario.velocityY}`);

        // Test button for jumping
        document.getElementById('jumpBtn').addEventListener('click', () => {
            addDebug('JUMP BUTTON clicked');
            if (canJump && gameState.isGameActive) {
                mario.velocityY = JUMP_POWER;
                mario.isJumping = true;
                canJump = false;
                addDebug('Button JUMP initiated!');
            } else {
                addDebug('Button: canJump=' + canJump + ', active=' + gameState.isGameActive);
            }
        });

        // Simpler keyboard handler - just track key states
        window.addEventListener('keydown', (e) => {
            const key = e.key;
            keyDisplay.textContent = 'Last Key: ' + (e.code || key);
            console.log('KEYDOWN EVENT:', key, 'Code:', e.code);
            addDebug('KEY DOWN: ' + (e.code || key));
            
            if (key === 'ArrowLeft') {
                keys.left = true;
                e.preventDefault();
            } 
            else if (key === 'ArrowRight') {
                keys.right = true;
                e.preventDefault();
            } 
            else if (key === ' ') {
                keys.space = true;
                e.preventDefault();
                console.log('SPACEBAR DETECTED IN EVENT HANDLER');
                addDebug('💨 SPACEBAR DOWN - keys.space set to true');
            }
        });

        window.addEventListener('keyup', (e) => {
            const key = e.key;
            
            if (key === 'ArrowLeft') {
                keys.left = false;
                e.preventDefault();
            } 
            else if (key === 'ArrowRight') {
                keys.right = false;
                e.preventDefault();
            } 
            else if (key === ' ') {
                keys.space = false;
                e.preventDefault();
                console.log('SPACEBAR RELEASED');
                addDebug('SPACEBAR UP');
            }
        });

        // Fallback: also attach to document and body
        document.addEventListener('keydown', (e) => {
            if (e.key === ' ') {
                keys.space = true;
                e.preventDefault();
                console.log('SPACEBAR DETECTED IN DOCUMENT HANDLER');
                addDebug('💨 SPACE DOWN (doc)');
            }
        });

        document.addEventListener('keyup', (e) => {
            if (e.key === ' ') {
                keys.space = false;
                e.preventDefault();
                console.log('SPACEBAR RELEASED (doc)');
            }
        });

        // Spawn obstacle
        function spawnObstacle() {
            obstacles.push({
                x: CONTAINER_WIDTH,
                y: CONTAINER_HEIGHT - GROUND_HEIGHT - 50,
                width: 30,
                height: 50,
                speed: 5
            });
        }

        // Spawn mushroom
        function spawnMushroom() {
            const fromRight = Math.random() > 0.5;
            mushrooms.push({
                x: fromRight ? CONTAINER_WIDTH : -35,
                y: Math.random() * (CONTAINER_HEIGHT - GROUND_HEIGHT - 60),
                width: 35,
                height: 35,
                speed: fromRight ? -4 : 4
            });
        }

        // Update Mario position
        function updateMario() {
            if (!gameState.isGameActive) return;

            // Horizontal movement
            if (keys.left && mario.x > 0) {
                mario.x -= 6;
            }
            if (keys.right && mario.x + mario.width < CONTAINER_WIDTH) {
                mario.x += 6;
            }

            // Vertical movement (gravity) - original system was correct!
            // Higher mario.y = higher on screen (CSS bottom positioning)
            // Jump sets positive velocity, gravity adds to it (slows jump down, then accelerates fall)
            mario.velocityY += GRAVITY;
            mario.y += mario.velocityY;

            // Ground collision
            if (mario.y + mario.height >= CONTAINER_HEIGHT - GROUND_HEIGHT) {
                mario.y = CONTAINER_HEIGHT - GROUND_HEIGHT - mario.height;
                mario.velocityY = 0;
                mario.isJumping = false;
                canJump = true;
            }

            // Check for jump input - only jump on NEW space press (transition from false to true)
            let spacePressed = keys.space && !lastSpaceState;
            
            if (spacePressed) {
                addDebug(`🔹 NEW SPACE PRESS! CanJump: ${canJump}, Active: ${gameState.isGameActive}`);
                console.log('Space pressed detected! canJump:', canJump);
            }
            
            if (spacePressed && canJump && gameState.isGameActive) {
                mario.velocityY = -JUMP_POWER;  // Negative velocity = upward jump
                mario.isJumping = true;
                canJump = false;
                addDebug('✅ JUMP EXECUTED! Velocity set to ' + (-JUMP_POWER));
                console.log('JUMP EXECUTED: velocityY =', mario.velocityY);
            }
            
            lastSpaceState = keys.space;

            // Update display
            marioElement.style.left = mario.x + 'px';
            marioElement.style.bottom = (CONTAINER_HEIGHT - mario.y - mario.height) + 'px';
        }

        // Update obstacles
        function updateObstacles() {
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= obstacles[i].speed;

                const obstacleEl = document.getElementById('obstacle-' + i);
                if (obstacleEl) {
                    obstacleEl.style.left = obstacles[i].x + 'px';
                }

                // Remove off-screen
                if (obstacles[i].x + obstacles[i].width < 0) {
                    if (obstacleEl) obstacleEl.remove();
                    obstacles.splice(i, 1);
                    gameState.score += 10; // Points for avoiding
                } else {
                    // Check collision - but allow landing on top
                    if (checkCollisionWithObstacle(mario, obstacles[i])) {
                        endGame();
                    }
                }
            }
        }

        // Update mushrooms
        function updateMushrooms() {
            for (let i = mushrooms.length - 1; i >= 0; i--) {
                mushrooms[i].x += mushrooms[i].speed;

                const mushroomEl = document.getElementById('mushroom-' + i);
                if (mushroomEl) {
                    mushroomEl.style.left = mushrooms[i].x + 'px';
                }

                // Remove off-screen
                if (mushrooms[i].x + mushrooms[i].width < 0 || mushrooms[i].x > CONTAINER_WIDTH) {
                    if (mushroomEl) mushroomEl.remove();
                    mushrooms.splice(i, 1);
                } else {
                    // Check collision with Mario
                    if (checkCollision(mario, mushrooms[i])) {
                        endGame();
                    }
                }
            }
        }

        // Collision detection - basic box collision
        function checkCollision(obj1, obj2) {
            return obj1.x < obj2.x + obj2.width &&
                   obj1.x + obj1.width > obj2.x &&
                   obj1.y < obj2.y + obj2.height &&
                   obj1.y + obj1.height > obj2.y;
        }

        // Platformer-style collision detection for obstacles
        // Only collide if Mario is NOT above the obstacle
        // Bounding boxes: mario occupies [mario.y, mario.y + mario.height]
        //                 obstacle occupies [obstacle.y, obstacle.y + obstacle.height]
        function checkCollisionWithObstacle(mario, obstacle) {
            // No collision if Mario is completely above the obstacle
            // Mario must be above the obstacle's top edge to be safe
            // (Mario's bounding box top must be >= obstacle's bounding box top)
            if (mario.y >= obstacle.y + obstacle.height) {
                return false; // Mario is completely above obstacle, safe to jump over
            }

            // Check normal box collision for all other cases
            return mario.x < obstacle.x + obstacle.width &&
                   mario.x + mario.width > obstacle.x &&
                   mario.y < obstacle.y + obstacle.height &&
                   mario.y + mario.height > obstacle.y;
        }

        // End game
        function endGame() {
            gameState.isGameActive = false;
            statusDisplay.textContent = 'Dead! Restarting...';
            gameOverScreen.classList.add('show');
            finalScoreDisplay.textContent = 'Score: ' + gameState.score;
            
            // Restart after 2 seconds
            setTimeout(() => {
                resetGame();
            }, 2000);
        }

        // Reset game
        function resetGame() {
            mario.x = MARIO_START_X;
            mario.y = CONTAINER_HEIGHT - GROUND_HEIGHT - 50;
            mario.velocityY = 0;
            mario.isJumping = false;
            canJump = true;
            lastSpaceState = false;
            keys.space = false;
            
            obstacles.forEach((_, i) => {
                const el = document.getElementById('obstacle-' + i);
                if (el) el.remove();
            });
            
            mushrooms.forEach((_, i) => {
                const el = document.getElementById('mushroom-' + i);
                if (el) el.remove();
            });
            
            obstacles = [];
            mushrooms = [];
            gameState.score = 0;
            gameState.time = 0;
            gameState.isGameActive = true;
            gameOverScreen.classList.remove('show');
            statusDisplay.textContent = 'Playing';
            scoreDisplay.textContent = '0';
            timerDisplay.textContent = '0';
        }

        // Render obstacles
        function renderObstacles() {
            obstacles.forEach((obs, i) => {
                let el = document.getElementById('obstacle-' + i);
                if (!el) {
                    el = document.createElement('div');
                    el.id = 'obstacle-' + i;
                    el.className = 'obstacle';
                    gameContainer.appendChild(el);
                }
                el.style.left = obs.x + 'px';
                el.style.bottom = (CONTAINER_HEIGHT - obs.y - obs.height) + 'px';
            });
        }

        // Render mushrooms
        function renderMushrooms() {
            mushrooms.forEach((mush, i) => {
                let el = document.getElementById('mushroom-' + i);
                if (!el) {
                    el = document.createElement('div');
                    el.id = 'mushroom-' + i;
                    el.className = 'mushroom';
                    gameContainer.appendChild(el);
                }
                el.style.left = mush.x + 'px';
                el.style.bottom = (CONTAINER_HEIGHT - mush.y - mush.height) + 'px';
            });
        }

        // Update UI
        function updateUI() {
            scoreDisplay.textContent = gameState.score;
            timerDisplay.textContent = gameState.time;
        }

        // Game loop
        let spawnObstacleCounter = 0;
        let spawnMushroomCounter = 0;
        let frameCount = 0;

        function gameLoop() {
            frameCount++;
            if (gameState.isGameActive) {
                // Force Mario to ground on first frame
                if (frameCount === 1) {
                    mario.y = CONTAINER_HEIGHT - GROUND_HEIGHT - mario.height;
                    mario.velocityY = 0;
                    addDebug('First frame: Mario reset to y=' + Math.round(mario.y));
                }
                updateMario();
                updateObstacles();
                updateMushrooms();
                renderObstacles();
                renderMushrooms();
                updateUI();

                // Debug output every 15 frames
                if (frameCount % 15 === 0) {
                    let obsInfo = '';
                    if (obstacles.length > 0) {
                        const obs = obstacles[0];
                        const marioAbove = mario.y > obs.y ? '✓ ABOVE' : '✗ BELOW';
                        obsInfo = ` | Obs: y=${Math.round(obs.y)} ${marioAbove}`;
                    }
                    addDebug(`Mario Y: ${Math.round(mario.y)} Jumping: ${mario.isJumping}${obsInfo}`);
                }

                // Spawn obstacles every 70 frames
                spawnObstacleCounter++;
                if (spawnObstacleCounter > 70) {
                    spawnObstacle();
                    spawnObstacleCounter = 0;
                }

                // Spawn mushrooms every 120 frames
                spawnMushroomCounter++;
                if (spawnMushroomCounter > 120) {
                    spawnMushroom();
                    spawnMushroomCounter = 0;
                }

                // Update time every 60 frames
                if (spawnObstacleCounter % 60 === 0) {
                    gameState.time++;
                    gameState.score += 1; // 1 point per second
                }
            }

            requestAnimationFrame(gameLoop);
        }

        // Initial render of Mario at ground level
        marioElement.style.left = mario.x + 'px';
        marioElement.style.bottom = (CONTAINER_HEIGHT - mario.y - mario.height) + 'px';
        addDebug(`Rendered: Mario at bottom=${Math.round(CONTAINER_HEIGHT - mario.y - mario.height)}px`);

        // Start game
        gameLoop();
    </script>
</body>
</html>
"""

class GameRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler for the game"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '':
            # Serve the game HTML
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(GAME_HTML.encode('utf-8'))
        else:
            # 404 for other paths
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        return

if __name__ == '__main__':
    server_address = ('localhost', 3030)
    httpd = HTTPServer(server_address, GameRequestHandler)
    
    print("=" * 60)
    print("🎮 Super Mario Obstacle Game Starting...")
    print("=" * 60)
    print("\n✅ Game is running at: http://localhost:3030")
    print("\n📖 Controls:")
    print("   ← → Arrow Keys: Move Mario left and right")
    print("   SPACEBAR: Jump")
    print("\n🎯 Objective:")
    print("   • Jump over brown obstacles")
    print("   • Avoid incoming mushrooms")
    print("   • Unlimited lives - game restarts on collision")
    print("   • Earn points by avoiding obstacles and surviving")
    print("\n💡 Press Ctrl+C to stop the game server")
    print("=" * 60 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Game server stopped. Thanks for playing!")
        httpd.server_close()
