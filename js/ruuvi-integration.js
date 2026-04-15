/**
 * Ruuvi Tag IoT Sensor Integration for Mario Game
 * Enables motion-based game controls and environmental difficulty adjustments
 * 
 * Features:
 * - Motion-based player controls (accelerometer)
 * - Environmental difficulty adjustment (temperature, humidity)
 * - Player engagement detection
 * - Real-time sensor data logging
 */

class RuuviTagGameIntegration {
  constructor(gameState) {
    this.gameState = gameState;
    this.device = null;
    this.server = null;
    this.characteristic = null;
    this.connected = false;
    this.sensorData = {
      motionX: 0,
      motionY: 0,
      motionZ: 0,
      temperature: 0,
      humidity: 0,
      pressure: 0,
      batteryVoltage: 0,
      movements: 0,
      measurementSequence: 0
    };
    this.lastMovementTime = Date.now();
    this.lastActivityLog = 0;
  }

  /**
   * Connect to nearby Ruuvi Tag device via Bluetooth
   */
  async connect() {
    try {
      console.log('🔍 Scanning for Ruuvi Tag devices...');
      
      const device = await navigator.bluetooth.requestDevice({
        filters: [
          { namePrefix: 'Ruuvi' },
          { manufacturer: { id: 0x0499 } }
        ]
      });

      console.log(`📡 Found device: ${device.name}`);
      
      const server = await device.gatt.connect();
      console.log('✅ Connected to GATT server');

      // Get manufacturer-specific data
      this.device = device;
      this.server = server;
      this.connected = true;

      // Listen for disconnection
      device.addEventListener('gattserverdisconnected', () => {
        this.onDisconnect();
      });

      // Start polling sensor data
      this.startPolling();
      
      return true;
    } catch (error) {
      console.error('❌ Failed to connect to Ruuvi Tag:', error);
      return false;
    }
  }

  /**
   * Start polling sensor data from Ruuvi Tag
   */
  startPolling() {
    this.pollingInterval = setInterval(() => {
      this.updateSensorData();
    }, 100);  // 100ms polling interval

    console.log('📊 Started sensor data polling');
  }

  /**
   * Update sensor data (simulated for demo, real data from BLE)
   */
  async updateSensorData() {
    // In production, this would read from actual BLE characteristic
    // For now, we'll use WebBluetooth advertisement data
    if (this.device) {
      try {
        // Simulated sensor data for demo
        this.sensorData = {
          motionX: (Math.random() - 0.5) * 20,
          motionY: (Math.random() - 0.5) * 20,
          motionZ: (Math.random() - 0.5) * 20,
          temperature: 20 + (Math.random() - 0.5) * 5,
          humidity: 60 + (Math.random() - 0.5) * 20,
          pressure: 1013 + (Math.random() - 0.5) * 10,
          batteryVoltage: 2800 + Math.random() * 400
        };

        // Update game based on sensor data
        this.updateGameInput();
        this.updateGameDifficulty();
        this.detectPlayerEngagement();
      } catch (error) {
        console.error('Error reading sensor data:', error);
      }
    }
  }

  /**
   * Update game input based on motion sensors
   */
  updateGameInput() {
    const { motionX, motionY, motionZ } = this.sensorData;

    // Motion threshold for controls
    const MOTION_THRESHOLD = 5;
    const JUMP_THRESHOLD = 15;

    // Left/Right movement - tilt device
    if (motionX > MOTION_THRESHOLD) {
      window.gameKeys = window.gameKeys || {};
      window.gameKeys.right = true;
    } else if (motionX < -MOTION_THRESHOLD) {
      window.gameKeys = window.gameKeys || {};
      window.gameKeys.left = true;
    } else {
      // Reset if centered
      if (window.gameKeys) {
        window.gameKeys.left = false;
        window.gameKeys.right = false;
      }
    }

    // Jump - shake/tap motion (high Z acceleration)
    if (motionZ > JUMP_THRESHOLD) {
      window.gameKeys = window.gameKeys || {};
      window.gameKeys.space = true;
      this.lastMovementTime = Date.now();
    }

    // Log sensor data to console (optional)
    this.logSensorActivity();
  }

  /**
   * Adjust game difficulty based on environmental data
   */
  updateGameDifficulty() {
    const { temperature, humidity } = this.sensorData;

    // Temperature = Speed multiplier
    let tempMultiplier = 1.0;
    if (temperature > 25) {
      tempMultiplier = 1.0 + (temperature - 25) * 0.05;
    } else if (temperature < 18) {
      tempMultiplier = 1.0 - (18 - temperature) * 0.05;
    }

    // Humidity = Spawn rate multiplier
    let humidityMultiplier = 1.0;
    if (humidity > 70) {
      humidityMultiplier = 1.0 + (humidity - 70) * 0.01;
    } else if (humidity < 40) {
      humidityMultiplier = 1.0 - (40 - humidity) * 0.01;
    }

    // Apply difficulty adjustments
    if (window.gameState) {
      // Note: These would interact with actual game constants
      window.gameState.difficultyMultiplier = {
        temperature: tempMultiplier,
        humidity: humidityMultiplier,
        combined: tempMultiplier * humidityMultiplier
      };
    }
  }

  /**
   * Detect player engagement level
   */
  detectPlayerEngagement() {
    const { motionX, motionY, motionZ } = this.sensorData;

    // Calculate total motion magnitude
    const totalMotion = Math.sqrt(motionX ** 2 + motionY ** 2 + motionZ ** 2);

    // Check if player is actively moving
    if (totalMotion > 10) {
      this.lastMovementTime = Date.now();
      
      if (window.gameState) {
        window.gameState.playerEngaged = true;
      }
    } else {
      // Check idle timeout (5 seconds)
      const idleTime = Date.now() - this.lastMovementTime;
      if (idleTime > 5000) {
        if (window.gameState) {
          window.gameState.playerEngaged = false;
        }
        
        // Optional: Pause game if idle
        if (window.pauseGame && this.gameState.isGameActive) {
          console.log('⏸️ Game paused due to inactivity');
          // window.pauseGame();
        }
      }
    }
  }

  /**
   * Log sensor activity for debugging
   */
  logSensorActivity() {
    const now = Date.now();
    if (now - this.lastActivityLog > 1000) {  // Log every 1 second
      const { temperature, humidity, motionX, motionY, motionZ } = this.sensorData;
      console.log(`📊 Ruuvi: Temp=${temperature.toFixed(1)}°C, Humidity=${humidity.toFixed(0)}%, Motion=(${motionX.toFixed(1)},${motionY.toFixed(1)},${motionZ.toFixed(1)})`);
      this.lastActivityLog = now;
    }
  }

  /**
   * Handle device disconnection
   */
  onDisconnect() {
    console.log('📡 Ruuvi Tag disconnected');
    this.connected = false;
    
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }

    // Pause game on disconnect
    if (this.gameState.isGameActive) {
      console.log('⚠️ Game paused - sensor disconnected');
      // window.pauseGame();
    }
  }

  /**
   * Get real-time sensor telemetry
   */
  getTelemetry() {
    return {
      connected: this.connected,
      device: this.device?.name || 'Not connected',
      sensors: this.sensorData,
      timestamp: Date.now()
    };
  }

  /**
   * Display telemetry in HUD overlay
   */
  displayTelemetryOverlay() {
    const telemetry = this.getTelemetry();
    
    // Create or update overlay
    let overlay = document.getElementById('ruuvi-telemetry');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'ruuvi-telemetry';
      overlay.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(0, 0, 0, 0.8);
        color: #0f0;
        padding: 15px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 12px;
        z-index: 1000;
        max-width: 300px;
      `;
      document.body.appendChild(overlay);
    }

    const { temperature, humidity, motionX, motionY, motionZ } = telemetry.sensors;
    overlay.innerHTML = `
      <div style="color: ${telemetry.connected ? '#0f0' : '#f00'}">
        📡 ${telemetry.device}
      </div>
      <div>🌡️ Temp: ${temperature.toFixed(1)}°C</div>
      <div>💧 Humidity: ${humidity.toFixed(0)}%</div>
      <div>📍 Motion X: ${motionX.toFixed(1)}</div>
      <div>📍 Motion Y: ${motionY.toFixed(1)}</div>
      <div>📍 Motion Z: ${motionZ.toFixed(1)}</div>
    `;
  }

  /**
   * Disconnect from Ruuvi Tag
   */
  disconnect() {
    if (this.device && this.device.gatt.connected) {
      this.device.gatt.disconnect();
      console.log('✋ Manually disconnected from Ruuvi Tag');
    }
  }
}

// Export for use in game
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RuuviTagGameIntegration;
}
