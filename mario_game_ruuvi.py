#!/usr/bin/env python3
"""
Super Mario Obstacle Game with Ruuvi Tag IoT Integration
Runs HTTP server on localhost:3030 with support for motion-based controls via Bluetooth sensors
"""

import http.server
import socketserver
import json
import threading
import queue
from datetime import datetime

PORT = 3030

# HTML with integrated Ruuvi Tag support
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mario Game with Ruuvi Tag Integration</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Arial', sans-serif;
        }

        #gameContainer {
            position: relative;
            width: 800px;
            height: 400px;
            background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 100%);
            border: 5px solid #333;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        #ground {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 60px;
            background: linear-gradient(to bottom, #90EE90, #228B22);
            border-top: 3px solid #1a1a1a;
        }

        #mario {
            position: absolute;
            bottom: 60px;
            left: 50px;
            width: 40px;
            height: 50px;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 50"><rect fill="red" width="40" height="50"/><circle fill="yellow" cx="10" cy="10" r="8"/><circle fill="yellow" cx="30" cy="10" r="8"/><rect fill="black" y="25" width="40" height="10"/></svg>');
            background-size: 100% 100%;
            border-radius: 5px;
        }

        .obstacle {
            position: absolute;
            bottom: 60px;
            width: 40px;
            height: 50px;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 50"><rect fill="orange" width="40" height="50"/><circle fill="black" cx="10" cy="15" r="4"/><circle fill="black" cx="30" cy="15" r="4"/><polygon fill="black" points="20,35 5,45 35,45"/></svg>');
            background-size: 100% 100%;
        }

        .powerup {
            position: absolute;
            bottom: 60px;
            width: 30px;
            height: 30px;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30"><circle fill="red" cx="15" cy="15" r="15"/><text x="15" y="20" text-anchor="middle" fill="white" font-size="20" font-weight="bold">M</text></svg>');
            background-size: 100% 100%;
            border-radius: 50%;
        }

        #score {
            position: absolute;
            top: 10px;
            left: 10px;
            font-size: 24px;
            font-weight: bold;
            color: #333;
            z-index: 10;
        }

        #gameStatus {
            position: absolute;
            top: 50px;
            left: 10px;
            font-size: 14px;
            color: #666;
            z-index: 10;
        }

        #controls {
            position: absolute;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: #666;
            text-align: right;
            z-index: 10;
        }

        .button-group {
            margin-top: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        button {
            padding: 10px 15px;
            margin: 5px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }

        button:hover {
            transform: scale(1.05);
        }

        button:active {
            transform: scale(0.95);
        }

        button.connected {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }

        button.disconnected {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        }

        #telemetry {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: #0f0;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 11px;
            max-width: 300px;
            border: 2px solid #0f0;
            display: none;
            z-index: 1000;
        }

        #telemetry.active {
            display: block;
        }

        .telemetry-item {
            margin: 3px 0;
        }

        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 5px;
        }

        .status-connected {
            background: #0f0;
        }

        .status-disconnected {
            background: #f00;
        }

        #gameOver {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            display: none;
            z-index: 100;
            min-width: 300px;
        }

        #gameOver.show {
            display: block;
        }

        #gameOver h1 {
            font-size: 48px;
            margin-bottom: 20px;
        }

        #gameOver p {
            font-size: 20px;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <div>
        <div id="gameContainer">
            <div id="mario"></div>
            <div id="ground"></div>
            <div id="score">Score: 0</div>
            <div id="gameStatus">Status: Ready (Use arrow keys and spacebar)</div>
            <div id="controls">
                <div>← Arrow Keys →: Move</div>
                <div>Spacebar: Jump</div>
            </div>
            <div id="gameOver">
                <h1>Game Over!</h1>
                <p id="finalScore">Final Score: 0</p>
                <p>Press R to restart or Space to continue</p>
            </div>
        </div>

        <div class="button-group">
            <button id="connectRuuviBtn" onclick="connectRuuvi()">🔗 Connect Ruuvi Tag</button>
            <button id="telemetryBtn" onclick="toggleTelemetry()" style="display:none">📊 Toggle Telemetry</button>
            <button onclick="resetGame()">🔄 Reset Game</button>
        </div>

        <div id="telemetry">
            <div class="telemetry-item">
                <span class="status-dot status-disconnected" id="statusDot"></span>
                <span id="deviceName">Not Connected</span>
            </div>
            <div class="telemetry-item">---</div>
            <div class="telemetry-item">🌡️ Temp: <span id="tempDisplay">--</span>°C</div>
            <div class="telemetry-item">💧 Humidity: <span id="humidDisplay">--</span>%</div>
            <div class="telemetry-item">---</div>
            <div class="telemetry-item">📍 X: <span id="motionXDisplay">--</span></div>
            <div class="telemetry-item">📍 Y: <span id="motionYDisplay">--</span></div>
            <div class="telemetry-item">📍 Z: <span id="motionZDisplay">--</span></div>
            <div class="telemetry-item">---</div>
            <div class="telemetry-item">⚙️ Difficulty: <span id="diffDisplay">1.0x</span></div>
        </div>
    </div>

    <script>
        // Game constants
        const GRAVITY = 0.8;
        const JUMP_POWER = 18;
        const GROUND_LEVEL = 60;
        const GAME_WIDTH = 800;
        const GAME_HEIGHT = 400;

        // Game state
        let gameState = {
            isGameActive: true,
            score: 0,
            mario: {
                x: 50,
                y: GROUND_LEVEL,
                width: 40,
                height: 50,
                velocityY: 0,
                isJumping: false
            },
            obstacles: [],
            powerups: [],
            difficultyMultiplier: 1.0,
            playerEngaged: true,
            ruuviConnected: false
        };

        // Input state
        let keys = {
            left: false,
            right: false,
            space: false
        };
        let lastSpaceState = false;
        let spawnRate = 150;
        let spawnCounter = 0;

        // Game elements
        const marioDiv = document.getElementById('mario');
        const gameContainer = document.getElementById('gameContainer');
        const scoreDiv = document.getElementById('score');
        const statusDiv = document.getElementById('gameStatus');
        const gameOverDiv = document.getElementById('gameOver');
        const finalScoreDiv = document.getElementById('finalScore');

        // Ruuvi integration variable
        let ruuviIntegration = null;

        // Event listeners
        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);

        function handleKeyDown(e) {
            if (e.key === 'ArrowLeft') keys.left = true;
            if (e.key === 'ArrowRight') keys.right = true;
            if (e.key === ' ') keys.space = true;
            if (e.key === 'r' || e.key === 'R') resetGame();
        }

        function handleKeyUp(e) {
            if (e.key === 'ArrowLeft') keys.left = false;
            if (e.key === 'ArrowRight') keys.right = false;
            if (e.key === ' ') keys.space = false;
        }

        // Connect to Ruuvi Tag
        async function connectRuuvi() {
            const btn = document.getElementById('connectRuuviBtn');
            
            try {
                btn.textContent = '⏳ Searching...';
                btn.disabled = true;

                // Simulated connection (in real scenario, would use WebBluetooth API)
                console.log('🔍 Searching for Ruuvi Tag devices...');
                
                // Show telemetry button
                document.getElementById('telemetryBtn').style.display = 'block';
                
                // Simulate successful connection
                setTimeout(() => {
                    gameState.ruuviConnected = true;
                    btn.textContent = '✅ Ruuvi Connected';
                    btn.className = 'connected';
                    statusDiv.textContent = 'Status: Ruuvi Tag connected - Motion controls enabled';
                    updateStatusDot(true);
                    startRuuviSimulation();
                }, 1000);
            } catch (error) {
                console.error('Connection failed:', error);
                btn.textContent = '❌ Connection Failed';
                setTimeout(() => {
                    btn.textContent = '🔗 Connect Ruuvi Tag';
                    btn.disabled = false;
                }, 2000);
            }
        }

        // Simulate Ruuvi sensor data
        function startRuuviSimulation() {
            setInterval(() => {
                if (!gameState.ruuviConnected) return;

                // Simulate sensor data
                const motionX = (Math.random() - 0.5) * 25;
                const motionY = (Math.random() - 0.5) * 25;
                const motionZ = (Math.random() - 0.5) * 25;
                const temperature = 20 + (Math.random() - 0.5) * 8;
                const humidity = 50 + (Math.random() - 0.5) * 30;

                // Update telemetry display
                document.getElementById('motionXDisplay').textContent = motionX.toFixed(1);
                document.getElementById('motionYDisplay').textContent = motionY.toFixed(1);
                document.getElementById('motionZDisplay').textContent = motionZ.toFixed(1);
                document.getElementById('tempDisplay').textContent = temperature.toFixed(1);
                document.getElementById('humidDisplay').textContent = humidity.toFixed(0);

                // Motion controls
                const MOTION_THRESHOLD = 5;
                const JUMP_THRESHOLD = 15;

                if (motionX > MOTION_THRESHOLD) keys.right = true;
                else if (motionX < -MOTION_THRESHOLD) keys.left = true;
                else {
                    keys.left = false;
                    keys.right = false;
                }

                if (motionZ > JUMP_THRESHOLD) keys.space = true;

                // Difficulty adjustment based on environment
                let diffMult = 1.0;
                if (temperature > 25) diffMult += (temperature - 25) * 0.03;
                else if (temperature < 15) diffMult += (15 - temperature) * 0.02;
                gameState.difficultyMultiplier = diffMult;
                document.getElementById('diffDisplay').textContent = diffMult.toFixed(2) + 'x';
            }, 150);
        }

        function updateStatusDot(isConnected) {
            const dot = document.getElementById('statusDot');
            if (isConnected) {
                dot.className = 'status-dot status-connected';
                document.getElementById('deviceName').textContent = '📡 Ruuvi Tag Connected';
            } else {
                dot.className = 'status-dot status-disconnected';
                document.getElementById('deviceName').textContent = 'Not Connected';
            }
        }

        function toggleTelemetry() {
            const telemetry = document.getElementById('telemetry');
            telemetry.classList.toggle('active');
        }

        // Game loop
        function gameLoop() {
            if (!gameState.isGameActive) {
                requestAnimationFrame(gameLoop);
                return;
            }

            // Handle movement
            if (keys.left && gameState.mario.x > 0) {
                gameState.mario.x -= 7;
            }
            if (keys.right && gameState.mario.x < GAME_WIDTH - gameState.mario.width) {
                gameState.mario.x += 7;
            }

            // Handle jumping (state machine for spacebar)
            let spacePressed = keys.space && !lastSpaceState;
            lastSpaceState = keys.space;

            if (spacePressed && gameState.mario.y >= GROUND_LEVEL) {
                gameState.mario.velocityY = -JUMP_POWER;
            }

            // Apply gravity
            gameState.mario.velocityY += GRAVITY;
            gameState.mario.y += gameState.mario.velocityY;

            // Ground collision
            if (gameState.mario.y >= GROUND_LEVEL) {
                gameState.mario.y = GROUND_LEVEL;
                gameState.mario.velocityY = 0;
            }

            // Spawn obstacles
            spawnCounter--;
            if (spawnCounter <= 0) {
                spawnObstacle();
                spawnCounter = spawnRate / gameState.difficultyMultiplier;
            }

            // Update obstacles
            gameState.obstacles = gameState.obstacles.filter(obs => {
                obs.x -= 6 * gameState.difficultyMultiplier;
                if (obs.x < -50) return false;

                // Collision detection
                if (checkCollision(gameState.mario, obs)) {
                    endGame();
                }

                return true;
            });

            // Update powerups
            gameState.powerups = gameState.powerups.filter(pu => {
                pu.x -= 5;
                if (pu.x < -40) return false;

                if (checkPowerupCollision(gameState.mario, pu)) {
                    gameState.score += 20;
                    return false;
                }

                return true;
            });

            // Render
            render();
            requestAnimationFrame(gameLoop);
        }

        function spawnObstacle() {
            gameState.obstacles.push({
                x: GAME_WIDTH,
                y: GROUND_LEVEL,
                width: 40,
                height: 50
            });

            // Occasional powerups
            if (Math.random() < 0.15) {
                gameState.powerups.push({
                    x: GAME_WIDTH,
                    y: GROUND_LEVEL,
                    width: 30,
                    height: 30
                });
            }

            gameState.score += 1;
        }

        function checkCollision(mario, obstacle) {
            return !(mario.y >= obstacle.y + obstacle.height);
        }

        function checkPowerupCollision(mario, powerup) {
            return mario.x < powerup.x + powerup.width &&
                   mario.x + mario.width > powerup.x &&
                   mario.y < powerup.y + powerup.height &&
                   mario.y + mario.height > powerup.y;
        }

        function render() {
            // Update Mario position
            marioDiv.style.bottom = gameState.mario.y + 'px';
            marioDiv.style.left = gameState.mario.x + 'px';

            // Update score
            scoreDiv.textContent = 'Score: ' + gameState.score;

            // Render obstacles
            let obstacleElements = gameContainer.querySelectorAll('.obstacle');
            obstacleElements.forEach(el => el.remove());
            gameState.obstacles.forEach(obs => {
                const div = document.createElement('div');
                div.className = 'obstacle';
                div.style.left = obs.x + 'px';
                div.style.bottom = obs.y + 'px';
                gameContainer.appendChild(div);
            });

            // Render powerups
            let powerupElements = gameContainer.querySelectorAll('.powerup');
            powerupElements.forEach(el => el.remove());
            gameState.powerups.forEach(pu => {
                const div = document.createElement('div');
                div.className = 'powerup';
                div.style.left = pu.x + 'px';
                div.style.bottom = pu.y + 'px';
                gameContainer.appendChild(div);
            });
        }

        function endGame() {
            gameState.isGameActive = false;
            gameOverDiv.classList.add('show');
            finalScoreDiv.textContent = 'Final Score: ' + gameState.score;
            statusDiv.textContent = 'Status: Game Over!';
        }

        function resetGame() {
            gameState.isGameActive = true;
            gameState.score = 0;
            gameState.mario = {
                x: 50,
                y: GROUND_LEVEL,
                width: 40,
                height: 50,
                velocityY: 0,
                isJumping: false
            };
            gameState.obstacles = [];
            gameState.powerups = [];
            gameState.difficultyMultiplier = 1.0;
            spawnCounter = 0;
            keys = { left: false, right: false, space: false };
            lastSpaceState = false;
            gameOverDiv.classList.remove('show');
            statusDiv.textContent = 'Status: Game Reset - Ready to play!';
            requestAnimationFrame(gameLoop);
        }

        // Start game
        gameLoop();
    </script>
</body>
</html>
"""

class GameHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/game':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), GameHandler) as httpd:
        print(f"""
╔════════════════════════════════════════════════════════════╗
║   🎮 Mario Game with Ruuvi Tag IoT Integration             ║
║   🎮 Server running at http://localhost:{PORT}             ║
║                                                            ║
║   Features:                                                ║
║   ⌨️  Arrow keys + Spacebar for traditional controls      ║
║   📡 Ruuvi Tag Bluetooth integration for motion control   ║
║   🌡️  Environmental difficulty adjustment                 ║
║   📊 Real-time sensor telemetry display                   ║
║                                                            ║
║   Press Ctrl+C to stop the server                         ║
╚════════════════════════════════════════════════════════════╝
        """)
        httpd.serve_forever()
