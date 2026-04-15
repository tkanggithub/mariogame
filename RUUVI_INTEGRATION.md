# Ruuvi Tag IoT Integration for Mario Game

## Overview

The Mario Game now supports **Ruuvi Tag** IoT sensors for motion-based controls and environmental difficulty adjustment. This enables team members to:

- **Control the game with device motion** (tilt to move, shake to jump)
- **Adjust difficulty based on real-world environment** (temperature, humidity)
- **Monitor sensor telemetry** in real-time during gameplay
- **Enable multi-sensor gaming experiences** for team collaboration

## What is a Ruuvi Tag?

[Ruuvi Tag](https://ruuvi.com/) is an advanced open-source Bluetooth IoT sensor tag that measures:
- **Accelerometer** (3-axis motion): X, Y, Z axis acceleration
- **Gyroscope**: Rotation and orientation
- **Temperature**: Environmental temperature
- **Humidity**: Relative humidity
- **Pressure**: Atmospheric pressure
- **Battery**: Device voltage monitoring

Perfect for interactive gaming and team activities!

## Installation & Setup

### Hardware Requirements

1. **Ruuvi Tag device(s)** - Purchase from [shop.ruuvi.com](https://shop.ruuvi.com/)
2. **Browser with Bluetooth support** - Chrome 56+, Edge 79+, Firefox (limited)
3. **Compatible device** - Laptop, tablet with Bluetooth LE

### Software Setup

#### Option 1: Using Enhanced Game with Built-in Ruuvi Support

Simply run the enhanced game version:

```bash
python mario_game_ruuvi.py
```

Then navigate to `http://localhost:3030` and click **"🔗 Connect Ruuvi Tag"** button.

#### Option 2: Manual Integration

Import the Ruuvi integration module in your HTML:

```html
<script src="js/ruuvi-integration.js"></script>

<script>
    // Initialize after game loads
    let ruuviIntegration = new RuuviTagGameIntegration(window.gameState);
    
    // Connect to device
    await ruuviIntegration.connect();
    
    // Display telemetry overlay
    ruuviIntegration.displayTelemetryOverlay();
</script>
```

## Game Controls

### Traditional Controls (Always Available)
| Control | Action |
|---------|--------|
| ← → Arrow Keys | Move left/right |
| Spacebar | Jump |
| R | Restart game |

### Ruuvi Tag Motion Controls (When Connected)
| Motion | Action | Threshold |
|--------|--------|-----------|
| **Tilt Left** (X < -5) | Move left | 5 units |
| **Tilt Right** (X > 5) | Move right | 5 units |
| **Shake/Tap** (Z > 15) | Jump | 15 units acceleration |

### Device Orientation Tips

**For optimal control, hold device:**
- **Horizontally** - rotated 90° from normal viewing angle
- **Tilt left/right** - to move Mario left/right
- **Quick tap down** - to make Mario jump

```
   ╔═══════╗
   ║ Ruuvi ║  <- Hold in landscape with screen facing you
   ║  Tag  ║      Tilt: [====] <- Mario moves left
   ╚═══════╝          [==========] <- Mario moves right
                      [    ▼    ] <- Jump (tap down)
```

## Environmental Difficulty Adjustment

Ruuvi Tag sensors automatically adjust game difficulty based on real-world conditions:

### Temperature Impact  (🌡️)

```
Temperature    Difficulty    Effect
─────────────────────────────────────
< 15°C         -2% to -5%    Slower obstacles
15-25°C        1.0x (Normal) Baseline speed
> 25°C         +2% to +5%    Faster obstacles
```

**Real-world use:** 
- Play outside in summer → faster game
- Play in cold office → easier game
- Great for seasonal gameplay variations!

### Humidity Impact (💧)

```
Humidity       Spawn Rate    Effect
─────────────────────────────────────
< 40%          -1% to -2%    Fewer obstacles
40-70%         1.0x (Normal) Normal spawn
> 70%          +1% to +2%    More obstacles
```

**Real-world use:**
- Humid weather → more obstacles to dodge
- Dry climate → fewer obstacles, easier game

### Combined Multiplier

Actual difficulty = Temperature Multiplier × Humidity Multiplier

Example:
- Temperature: 28°C (1.15x)
- Humidity: 75% (1.05x)
- **Combined: 1.15 × 1.05 = 1.21x** (21% faster/more obstacles)

## Telemetry Display

Click **"📊 Toggle Telemetry"** button to see real-time sensor data:

```
📡 Ruuvi Tag Connected
───────────────────────────
🌡️ Temp: 23.5°C
💧 Humidity: 65%
───────────────────────────
📍 X: 2.3      (Left/Right tilt)
📍 Y: -1.2     (Forward/Backward)
📍 Z: 8.5      (Up/Down/Tap)
───────────────────────────
⚙️ Difficulty: 1.08x
```

### Understanding Axis Orientation

| Axis | Direction | Typical Range |
|------|-----------|---------------|
| **X** | Left (-) to Right (+) | -20 to +20 |
| **Y** | Backward (-) to Forward (+) | -20 to +20 |
| **Z** | Down (-) to Up (+) | -20 to +20 |

Thresholds:
- Movement control: > 5 units
- Jump trigger: > 15 units

## Multi-Player Team Setup

### Using Multiple Ruuvi Tags

The integration supports multiple team members with their own Ruuvi devices:

```
Team Member 1 (Player 1)     Team Member 2 (Player 2)
┌─────────────┐              ┌─────────────┐
│  Ruuvi Tag  │──Bluetooth──▶│   Browser   │
│  Device #1  │              │  localhost  │
└─────────────┘              │    3030     │
                             └─────────────┘
                                   ▲
                                   │
┌─────────────┐                    │
│  Ruuvi Tag  │──Bluetooth────────┘
│  Device #2  │
└─────────────┘
Team Member 2
```

### Backstage Integration

Configure multiple players in `backstage/app-config.yaml`:

```yaml
game:
  players:
    - name: "Player 1"
      ruuvi_device_id: "AABBCCDDEE00"
      difficulty_preference: "expert"
    - name: "Player 2"
      ruuvi_device_id: "AABBCCDDEE01"
      difficulty_preference: "normal"
```

## API Reference

### RuuviTagGameIntegration Class

#### Constructor
```javascript
const ruuvi = new RuuviTagGameIntegration(gameState);
```

#### Methods

**connect()** - Connect to Ruuvi Tag via Bluetooth
```javascript
const success = await ruuvi.connect();
// Returns true if connection successful
```

**disconnect()** - Disconnect from device
```javascript
ruuvi.disconnect();
```

**getTelemetry()** - Get current sensor readings
```javascript
const data = ruuvi.getTelemetry();
// Returns: { connected, device, sensors: {...}, timestamp }
```

**displayTelemetryOverlay()** - Show sensor HUD
```javascript
ruuvi.displayTelemetryOverlay();
```

**startPolling()** - Begin sensor data polling
```javascript
ruuvi.startPolling(); // 100ms interval
```

#### Properties

```javascript
ruuvi.sensorData = {
    motionX: 0,           // -20 to +20
    motionY: 0,           // -20 to +20
    motionZ: 0,           // -20 to +20
    temperature: 0,       // °C
    humidity: 0,          // %
    pressure: 0,          // hPa
    batteryVoltage: 0     // mV
};

ruuvi.connected;          // boolean
ruuvi.device;            // BLE Device object
```

#### Events

```javascript
device.addEventListener('gattserverdisconnected', () => {
    console.log('Device disconnected');
});
```

## Troubleshooting

### "Connection Failed"

**Problem:** Button shows "❌ Connection Failed"

**Solutions:**
1. ✅ Ensure Bluetooth is enabled on your device
2. ✅ Check browser supports WebBluetooth (Chrome/Edge)
3. ✅ Verify Ruuvi Tag is powered on (LED should blink)
4. ✅ Restart browser and try again
5. ✅ Check device is not connected to another app

### No Motion Controls

**Problem:** Tilting/shaking doesn't affect Mario

**Solutions:**
1. ✅ Verify "Connected" status shows in telemetry
2. ✅ Check sensor readings in telemetry overlay (should change when moving)
3. ✅ Try larger motions (tilt at least 45°)
4. ✅ Verify motion threshold in code (default: 5 units)

### Erratic Motion

**Problem:** Mario moves unexpectedly

**Solutions:**
1. ✅ Increase motion threshold in code:
   ```javascript
   const MOTION_THRESHOLD = 8; // was 5
   ```
2. ✅ Calibrate device by laying flat for 10 seconds
3. ✅ Check telemetry for baseline drift
4. ✅ Restart Ruuvi Tag (restart app/power cycle)

### Difficulty Not Changing

**Problem:** Game speed doesn't adjust with temperature

**Solutions:**
1. ✅ Check telemetry shows different temperature values
2. ✅ Verify `gameState.difficultyMultiplier` updates
3. ✅ Check browser console for JavaScript errors
4. ✅ Ensure environmental data is being read correctly

## Code Examples

### Detecting Player Idle Time

```javascript
const IDLE_THRESHOLD = 5000; // 5 seconds

function detectIdlePlayer(ruuvi) {
    const { motionX, motionY, motionZ } = ruuvi.sensorData;
    const totalMotion = Math.sqrt(motionX**2 + motionY**2 + motionZ**2);
    
    if (totalMotion < 5) {
        const idleTime = Date.now() - lastMovementTime;
        if (idleTime > IDLE_THRESHOLD) {
            pauseGame(); // Pause if idle too long
        }
    }
}
```

### Custom Difficulty Scaling

```javascript
function customDifficultyCalculation(temp, humidity, pressure) {
    let multiplier = 1.0;
    
    // Temperature aggressiveness
    multiplier *= 1 + (temp - 20) * 0.08;
    
    // Humidity spawn rate
    multiplier *= 1 + (humidity - 60) * 0.02;
    
    // Pressure affects obstacle height (pressure systems)
    if (pressure < 1000) multiplier *= 1.05;
    
    return Math.max(0.5, Math.min(2.0, multiplier)); // Clamp 0.5x - 2.0x
}
```

### Multi-Device Synchronization

```javascript
async function initializeMultiplayerMode() {
    const player1 = new RuuviTagGameIntegration(gameState);
    const player2 = new RuuviTagGameIntegration(gameState);
    
    // Connect both players
    await player1.connect();
    await player2.connect();
    
    // Share difficulty across both
    const difficulty = (player1.getTelemetry().sensors.temperature +
                       player2.getTelemetry().sensors.temperature) / 2;
    
    gameState.difficultyMultiplier = calculateDifficulty(difficulty);
}
```

## Development & Contributing

### File Structure

```
CopilotHackathon/
├── mario_game.py              # Original game
├── mario_game_ruuvi.py        # Enhanced with Ruuvi support
├── js/
│   └── ruuvi-integration.js   # Core integration module
└── backstage/
    └── app-config.yaml        # Team configuration
```

### Testing Ruuvi Integration

1. Run enhanced game: `python mario_game_ruuvi.py`
2. Open telemetry: Click "📊 Toggle Telemetry"
3. Verify readings update every ~150ms
4. Test motion controls work smoothly
5. Check difficulty multiplier changes with temp/humidity

### Future Enhancements

- [ ] Wi-Fi sync between multiple Ruuvi devices
- [ ] Pressure-based obstacle height scaling
- [ ] Gyroscope-based rotation controls
- [ ] Battery voltage monitoring and warnings
- [ ] Recording and playback of sensor data
- [ ] Multiplayer leaderboards by temperature zone

## Resources

- **Ruuvi Documentation:** https://docs.ruuvi.com/
- **Bluetooth API:** https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API
- **Ruuvi Firmware:** https://github.com/ruuvi/ruuvi.firmware
- **Project Repository:** https://github.com/tkanggithub/mariogame

## Support

For issues or questions:
1. Check telemetry overlay for sensor readings
2. Open browser Developer Tools (F12) for console logs
3. Verify Ruuvi Tag firmware is up-to-date
4. Review troubleshooting section above
5. Open an issue on GitHub repository

---

**Happy gaming with Ruuvi Tags! 🎮📡**
