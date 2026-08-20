/**
 * Sleeper Class - Immersive Indian Railway Experience
 * Premium Fullscreen Skeuomorphic Controls & Cozy Audio Engine
 */

class ImmersiveAudioEngine {
  constructor() {
    this.ctx = null;
    this.initialized = false;

    // Nodes
    this.masterGain = null;
    this.trackRumble = null;
    this.trackRumbleGain = null;
    this.fanHum = null;
    this.fanGain = null;
    this.radioStatic = null;
    this.radioStaticGain = null;
    this.rainNode = null;
    this.rainGain = null;

    // PA system simulation nodes
    this.paStaticGain = null;
    this.paMainsHum = null;
    this.paStaticNoise = null;

    // Synthesized Noise Buffer
    this.noiseBuffer = null;

    // State Variables
    this.trainSpeedVal = 1.0; 
    this.targetTrainSpeedVal = 1.0; 
    this.fanSpeedVal = 0.0; 
    this.targetFanSpeedVal = 0.0;
    this.radioTuning = 0.5; 
    this.isRaining = false;

    this.activeHorn = null;
    this.synthInterval = null;
  }

  init() {
    if (this.initialized) return;

    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContextClass();

    // Master Gain (Cozy level)
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.setValueAtTime(0.5, this.ctx.currentTime); 
    this.masterGain.connect(this.ctx.destination);

    // Generate White Noise Buffer
    this.generateNoiseBuffer();
    // Setup Audio Units (Only weather and static for cottage, no train rumble/clacking)
    this.setupFanHum();
    this.setupRadioStatic();
    this.setupRain();
    this.setupWind();
    
    this.targetTrainSpeedVal = trainTypes[state.trainType].speed;
    this.trainSpeedVal = this.targetTrainSpeedVal;

    this.initialized = true;
    console.log("Cozy Ambient Audio Engine Initialized.");
  }

  resume() {
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  generateNoiseBuffer() {
    const size = 2 * this.ctx.sampleRate;
    this.noiseBuffer = this.ctx.createBuffer(1, size, this.ctx.sampleRate);
    const data = this.noiseBuffer.getChannelData(0);
    for (let i = 0; i < size; i++) {
      data[i] = Math.random() * 2 - 1;
    }
  }

  // 1. Train Rumble Synth (Soothing, low rumbling)
  setupTrackRumble() {
    this.trackRumble = this.ctx.createBufferSource();
    this.trackRumble.buffer = this.noiseBuffer;
    this.trackRumble.loop = true;

    const lowpass = this.ctx.createBiquadFilter();
    lowpass.type = 'lowpass';
    lowpass.frequency.setValueAtTime(55, this.ctx.currentTime);

    this.trackRumbleGain = this.ctx.createGain();
    this.trackRumbleGain.gain.setValueAtTime(0.12, this.ctx.currentTime); 

    this.trackRumble.connect(lowpass);
    lowpass.connect(this.trackRumbleGain);
    this.trackRumbleGain.connect(this.masterGain);

    this.trackRumble.start(0);
  }

  // 2. Fan Hum Synth
  setupFanHum() {
    this.fanHum = this.ctx.createOscillator();
    this.fanHum.type = 'sine';
    this.fanHum.frequency.setValueAtTime(45, this.ctx.currentTime);

    this.fanGain = this.ctx.createGain();
    this.fanGain.gain.setValueAtTime(0, this.ctx.currentTime);

    this.fanHum.connect(this.fanGain);
    this.fanGain.connect(this.masterGain);

    this.fanHum.start(0);
  }

  // 3. Radio Static Synth
  setupRadioStatic() {
    this.radioStatic = this.ctx.createBufferSource();
    this.radioStatic.buffer = this.noiseBuffer;
    this.radioStatic.loop = true;

    const bandpass = this.ctx.createBiquadFilter();
    bandpass.type = 'bandpass';
    bandpass.frequency.setValueAtTime(1600, this.ctx.currentTime);
    bandpass.Q.setValueAtTime(1.0, this.ctx.currentTime);

    this.radioStaticGain = this.ctx.createGain();
    this.radioStaticGain.gain.setValueAtTime(0.01, this.ctx.currentTime); 

    this.radioStatic.connect(bandpass);
    bandpass.connect(this.radioStaticGain);
    this.radioStaticGain.connect(this.masterGain);

    this.radioStatic.start(0);
  }

  // 4. Rainy Weather Synth
  setupRain() {
    this.rainNode = this.ctx.createBufferSource();
    this.rainNode.buffer = this.noiseBuffer;
    this.rainNode.loop = true;

    const lowpass = this.ctx.createBiquadFilter();
    lowpass.type = 'lowpass';
    lowpass.frequency.setValueAtTime(1100, this.ctx.currentTime);

    this.rainGain = this.ctx.createGain();
    this.rainGain.gain.setValueAtTime(0, this.ctx.currentTime);

    this.rainNode.connect(lowpass);
    lowpass.connect(this.rainGain);
    this.rainGain.connect(this.masterGain);

    this.rainNode.start(0);
  }

  // 4b. Cozy Whistling Wind Draft Synth
  setupWind() {
    this.windNode = this.ctx.createBufferSource();
    this.windNode.buffer = this.noiseBuffer;
    this.windNode.loop = true;

    this.windFilter = this.ctx.createBiquadFilter();
    this.windFilter.type = 'bandpass';
    this.windFilter.frequency.setValueAtTime(400, this.ctx.currentTime);
    this.windFilter.Q.setValueAtTime(8.0, this.ctx.currentTime); // High resonance for a whistling galelike sound

    this.windGain = this.ctx.createGain();
    this.windGain.gain.setValueAtTime(0, this.ctx.currentTime);

    this.windNode.connect(this.windFilter);
    this.windFilter.connect(this.windGain);
    this.windGain.connect(this.masterGain);

    this.windNode.start(0);
  }

  // 5. PA speaker static hum simulator
  setupPASpeakerStatic() {
    this.paStaticGain = this.ctx.createGain();
    this.paStaticGain.gain.setValueAtTime(0, this.ctx.currentTime);

    // 50Hz AC Mains Hum
    this.paMainsHum = this.ctx.createOscillator();
    this.paMainsHum.type = 'triangle';
    this.paMainsHum.frequency.setValueAtTime(50, this.ctx.currentTime);

    const humFilter = this.ctx.createBiquadFilter();
    humFilter.type = 'lowpass';
    humFilter.frequency.setValueAtTime(120, this.ctx.currentTime);

    // Random crackle source
    this.paStaticNoise = this.ctx.createBufferSource();
    this.paStaticNoise.buffer = this.noiseBuffer;
    this.paStaticNoise.loop = true;

    const crackleFilter = this.ctx.createBiquadFilter();
    crackleFilter.type = 'bandpass';
    crackleFilter.frequency.setValueAtTime(2200, this.ctx.currentTime);
    crackleFilter.Q.setValueAtTime(2.0, this.ctx.currentTime);

    this.paMainsHum.connect(humFilter);
    humFilter.connect(this.paStaticGain);

    this.paStaticNoise.connect(crackleFilter);
    crackleFilter.connect(this.paStaticGain);

    this.paStaticGain.connect(this.masterGain);

    this.paMainsHum.start(0);
    this.paStaticNoise.start(0);
  }

  // Triggers background PA static when voice announcements play
  triggerPAStatic(active, durationMs = 0) {
    if (!this.initialized) return;
    const now = this.ctx.currentTime;
    
    if (active) {
      this.paStaticGain.gain.cancelScheduledValues(now);
      this.paStaticGain.gain.setValueAtTime(0, now);
      this.paStaticGain.gain.linearRampToValueAtTime(0.035, now + 0.15); 
      
      if (durationMs > 0) {
        setTimeout(() => this.triggerPAStatic(false), durationMs);
      }
    } else {
      this.paStaticGain.gain.cancelScheduledValues(now);
      this.paStaticGain.gain.setValueAtTime(this.paStaticGain.gain.value, now);
      this.paStaticGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.4); 
    }
  }

  startTrackClackingLoop() {
    const triggerClack = () => {
      if (!this.initialized || this.trainSpeedVal < 0.15 || state.activeRoute !== 'hindi') {
        scheduleNext();
        return;
      }
      const now = this.ctx.currentTime;
      const vol = this.trainSpeedVal * 0.045; 

      const click = () => {
        const source = this.ctx.createBufferSource();
        source.buffer = this.noiseBuffer;

        const bp = this.ctx.createBiquadFilter();
        bp.type = 'bandpass';
        bp.frequency.setValueAtTime(950, now);
        bp.Q.setValueAtTime(3.5, now);

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(vol, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);

        source.connect(bp);
        bp.connect(gain);
        gain.connect(this.masterGain);

        source.start(now);
        source.stop(now + 0.06);
      };

      const puff = () => {
        const source = this.ctx.createBufferSource();
        source.buffer = this.noiseBuffer;
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(150 + Math.random() * 80, now);
        
        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(state.isAmbienceMuted ? 0 : 0.06, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        
        source.connect(filter);
        filter.connect(gain);
        gain.connect(this.masterGain);
        source.start(now);
        source.stop(now + 0.16);
      };

      if (state.trainType === 'steam') {
        puff();
      } else {
        click();
        setTimeout(() => click(), 120);
      }

      scheduleNext();
    };

    const scheduleNext = () => {
      if (this.clackTimer) clearTimeout(this.clackTimer);
      let interval = 3000;
      if (this.trainSpeedVal > 0.1) {
        if (state.trainType === 'steam') {
          interval = 550 / this.trainSpeedVal; 
        } else {
          interval = 1200 / this.trainSpeedVal;
        }
      }
      this.clackTimer = setTimeout(triggerClack, interval);
    };

    scheduleNext();
  }

  startSqueakLoop() {
    const triggerSqueak = () => {
      if (!this.initialized || this.fanSpeedVal < 0.1) {
        scheduleNext();
        return;
      }

      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      osc.type = 'sine';
      
      const pitch = 2200 + (this.fanSpeedVal * 200) + Math.random() * 150;
      osc.frequency.setValueAtTime(pitch, now);

      const gain = this.ctx.createGain();
      const vol = this.fanSpeedVal * 0.0015; 
      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(vol, now + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.07);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.08);

      scheduleNext();
    };

    const scheduleNext = () => {
      if (this.squeakTimer) clearTimeout(this.squeakTimer);
      let min = 2500;
      let max = 6500;
      if (this.fanSpeedVal > 0.1) {
        min = 1200 / this.fanSpeedVal;
        max = 3500 / this.fanSpeedVal;
      }
      const delay = min + Math.random() * (max - min);
      this.squeakTimer = setTimeout(triggerSqueak, delay);
    };

    scheduleNext();
  }

  // 🎹 Safe Synthesized Cassette Tape Audio
  startSynthTape() {
    if (this.synthInterval) clearInterval(this.synthInterval);
    
    // Nostalgic warm chords progression (Cmaj7 -> Fmaj7 -> G7 -> Em7)
    const chords = [
      [130.81, 164.81, 196.00, 246.94], // Cmaj7
      [174.61, 220.00, 261.63, 329.63], // Fmaj7
      [196.00, 246.94, 293.66, 349.23], // G7
      [164.81, 196.00, 246.94, 293.66]  // Em7
    ];
    
    let chordIndex = 0;
    
    const playChord = () => {
      if (!this.initialized || !state.isPlaying || !state.useSynthFallback) return;
      const now = this.ctx.currentTime;
      const chord = chords[chordIndex];
      
      chord.forEach((freq, idx) => {
        const noteDelay = idx * 0.18; 
        const osc = this.ctx.createOscillator();
        const oscGain = this.ctx.createGain();
        
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now + noteDelay);
        
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(650, now + noteDelay); 
        
        oscGain.gain.setValueAtTime(0, now + noteDelay);
        oscGain.gain.linearRampToValueAtTime(0.08 * (state.volume / 100), now + noteDelay + 0.35);
        oscGain.gain.exponentialRampToValueAtTime(0.0001, now + noteDelay + 2.5);
        
        osc.connect(filter);
        filter.connect(oscGain);
        oscGain.connect(this.masterGain);
        
        osc.start(now + noteDelay);
        osc.stop(now + noteDelay + 2.6);
      });
      
      chordIndex = (chordIndex + 1) % chords.length;
    };
    
    playChord();
    this.synthInterval = setInterval(playChord, 3200);
  }

  stopSynthTape() {
    if (this.synthInterval) {
      clearInterval(this.synthInterval);
      this.synthInterval = null;
    }
  }

  playHorn() {
    this.resume();
    if (!this.initialized) this.init();

    const now = this.ctx.currentTime;
    
    // Choose frequencies and wave types based on active train type
    let freqs = [370, 440, 554]; // Default Rajdhani Multi-tone
    let hornType = 'modern';
    
    if (state.trainType === 'passenger') {
      freqs = [220, 277, 330]; // Vintage diesel chord
      hornType = 'vintage';
    } else if (state.trainType === 'goods') {
      freqs = [150, 180, 220]; // Heavy, low freight diesel rumble
      hornType = 'freight';
    } else if (state.trainType === 'steam') {
      freqs = [620, 880]; // High-pitched steam whistle
      hornType = 'steam-whistle';
    }

    const oscillators = [];
    const hornGainNode = this.ctx.createGain();
    hornGainNode.gain.setValueAtTime(0, now);
    hornGainNode.gain.linearRampToValueAtTime(0.55, now + 0.06); 

    const bpFilter = this.ctx.createBiquadFilter();
    bpFilter.type = 'bandpass';
    
    if (hornType === 'steam-whistle') {
      bpFilter.frequency.setValueAtTime(1500, now);
      bpFilter.Q.setValueAtTime(0.8, now);
    } else {
      bpFilter.frequency.setValueAtTime(950, now);
      bpFilter.Q.setValueAtTime(1.2, now);
    }

    const shaper = this.ctx.createWaveShaper();
    shaper.curve = this.makeDistortionCurve(hornType === 'steam-whistle' ? 5 : 22);
    shaper.oversample = '4x';

    // Synthesize background steam hiss for heritage steam horn
    let steamNoise = null;
    if (hornType === 'steam-whistle') {
      steamNoise = this.ctx.createBufferSource();
      steamNoise.buffer = this.noiseBuffer;
      steamNoise.loop = true;
      
      const bpSteam = this.ctx.createBiquadFilter();
      bpSteam.type = 'bandpass';
      bpSteam.frequency.setValueAtTime(2400, now);
      bpSteam.Q.setValueAtTime(2.0, now);
      
      const steamGain = this.ctx.createGain();
      steamGain.gain.setValueAtTime(0.04, now);
      
      steamNoise.connect(bpSteam);
      bpSteam.connect(steamGain);
      steamGain.connect(hornGainNode);
      steamNoise.start(now);
    }

    freqs.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const detune = (Math.random() * 8) - 4;
      osc.frequency.setValueAtTime(freq, now);
      osc.detune.setValueAtTime(detune, now);
      
      if (hornType === 'steam-whistle') {
        osc.type = 'sine'; // Steam whistle sounds pure
      } else {
        if (idx === 0) osc.type = 'sawtooth';
        else if (idx === 1) osc.type = 'triangle';
        else osc.type = 'sine';
      }

      osc.connect(hornGainNode);
      oscillators.push(osc);
      osc.start(now);
    });

    hornGainNode.connect(shaper);
    shaper.connect(bpFilter);
    bpFilter.connect(this.masterGain);

    return {
      stop: () => {
        const stopTime = this.ctx.currentTime;
        hornGainNode.gain.cancelScheduledValues(stopTime);
        hornGainNode.gain.setValueAtTime(hornGainNode.gain.value, stopTime);
        hornGainNode.gain.exponentialRampToValueAtTime(0.001, stopTime + 0.18);
        
        if (steamNoise) {
          try { steamNoise.stop(stopTime + 0.2); } catch(e) {}
        }
        setTimeout(() => {
          oscillators.forEach(osc => {
            try { osc.stop(); } catch(e) {}
          });
        }, 250);
      }
    };
  }

  makeDistortionCurve(amount) {
    const k = typeof amount === 'number' ? amount : 50;
    const n = 44100;
    const curve = new Float32Array(n);
    const deg = Math.PI / 180;
    for (let i = 0; i < n; ++i) {
      const x = (i * 2) / n - 1;
      curve[i] = ((3 + k) * x * 20 * deg) / (Math.PI + k * Math.abs(x));
    }
    return curve;
  }

  playSwitchClick() {
    if (!this.initialized) return;
    const now = this.ctx.currentTime;
    
    const clickOsc = this.ctx.createOscillator();
    clickOsc.type = 'triangle';
    clickOsc.frequency.setValueAtTime(250, now);
    clickOsc.frequency.exponentialRampToValueAtTime(80, now + 0.02);

    const hpFilter = this.ctx.createBiquadFilter();
    hpFilter.type = 'highpass';
    hpFilter.frequency.setValueAtTime(400, now);

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.02);

    clickOsc.connect(hpFilter);
    hpFilter.connect(gain);
    gain.connect(this.masterGain);

    clickOsc.start(now);
    clickOsc.stop(now + 0.02);
  }

  playShutterClink() {
    if (!this.initialized) return;
    const now = this.ctx.currentTime;
    
    const osc1 = this.ctx.createOscillator();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(2800, now);

    const osc2 = this.ctx.createOscillator();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(3200, now);

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.02, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.06);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(this.masterGain);

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 0.08);
    osc2.stop(now + 0.08);
  }

  playEmergencyBrakeScreech() {
    if (!this.initialized) this.init();
    const now = this.ctx.currentTime;
    const dur = 4.2;

    const osc = this.ctx.createOscillator();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(3400, now);
    osc.frequency.exponentialRampToValueAtTime(200, now + dur);

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(2800, now);
    filter.frequency.exponentialRampToValueAtTime(400, now + dur);
    filter.Q.setValueAtTime(3.0, now);

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(0.12, now + 0.25);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + dur);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.masterGain);

    osc.start(now);
    osc.stop(now + dur + 0.1);
  }

  tick() {
    // 1. Math speed interpolations (Always run so scrolling updates instantly on page load!)
    const fanDiff = this.targetFanSpeedVal - this.fanSpeedVal;
    if (Math.abs(fanDiff) > 0.005) {
      this.fanSpeedVal += fanDiff * 0.015;
    } else {
      this.fanSpeedVal = this.targetFanSpeedVal;
    }

    const trainDiff = this.targetTrainSpeedVal - this.trainSpeedVal;
    if (Math.abs(trainDiff) > 0.005) {
      this.trainSpeedVal += trainDiff * 0.06;
    } else {
      this.trainSpeedVal = this.targetTrainSpeedVal;
    }

    // 2. Web Audio nodes updates (Deferred until initialized)
    if (!this.initialized) return;

    const now = this.ctx.currentTime;

    // Update Fan Hum Synthesizer (Cozy level)
    if (this.fanGain && this.fanHum) {
      const humVol = state.isAmbienceMuted ? 0 : (this.fanSpeedVal * 0.06); 
      const humFreq = 40 + (this.fanSpeedVal * 18);
      this.fanGain.gain.setTargetAtTime(humVol, now, 0.2);
      this.fanHum.frequency.setTargetAtTime(humFreq, now, 0.5);
    }

    // Update Train Rumble (Cozy level)
    if (this.trackRumbleGain) {
      const rumbleVol = (state.isAmbienceMuted || state.activeRoute !== 'hindi') ? 0 : (this.trainSpeedVal * 0.08); 
      this.trackRumbleGain.gain.setTargetAtTime(rumbleVol, now, 0.4);
    }

    // Update Static Radio (Cozy level)
    if (this.radioStaticGain) {
      const staticVol = state.isAmbienceMuted ? 0 : ((1 - this.radioTuning) * 0.012); 
      this.radioStaticGain.gain.setTargetAtTime(staticVol, now, 0.15);
    }

    // Update Rain sound
    if (this.rainGain) {
      const rainVol = (state.isAmbienceMuted || !state.isRaining) ? 0 : 0.045; 
      this.rainGain.gain.setTargetAtTime(rainVol, now, 0.5);

      // Synthesize realistic random raindrop clicking/pattering against the glass window pane
      if (state.isRaining && !state.isAmbienceMuted && Math.random() < 0.18) {
        const clickOsc = this.ctx.createOscillator();
        const clickGain = this.ctx.createGain();
        clickOsc.type = 'sine';
        
        // Random high frequency tap (monsoon hitting glass)
        const tapFreq = 1600 + Math.random() * 800;
        clickOsc.frequency.setValueAtTime(tapFreq, now);
        clickOsc.frequency.exponentialRampToValueAtTime(700, now + 0.015);
        
        const tapVol = 0.003 + Math.random() * 0.007; // Very soft, cozy clicks
        clickGain.gain.setValueAtTime(tapVol * (state.volume / 100), now);
        clickGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.02);
        
        clickOsc.connect(clickGain);
        clickGain.connect(this.masterGain);
        clickOsc.start(now);
        clickOsc.stop(now + 0.03);
      }
    }

    // Update Whistling Wind (Cozy sweeping filter on white noise)
    if (this.windFilter && this.windGain) {
      const windVol = (state.isAmbienceMuted || !state.isWindy) ? 0 : 0.035;
      this.windGain.gain.setTargetAtTime(windVol, now, 0.45);
      
      // Sweep whistling wind cutoff frequency slowly using overlapping sines
      const sweepFreq = 380 + Math.sin(now * 0.4) * 140 + Math.sin(now * 0.11) * 60;
      this.windFilter.frequency.setTargetAtTime(sweepFreq, now, 0.3);
    }
  }

  setTuning(quality) {
    this.radioTuning = quality;
  }

  setWeather(raining) {
    this.isRaining = raining;
  }
}

// Instantiate Engine
const audio = new ImmersiveAudioEngine();

function getInitialRouteFromPath() {
  const path = window.location.pathname.replace(/^\/|\/$/g, '').toLowerCase();
  if (['punjab', 'jammu', 'english'].includes(path)) return path;
  return 'hindi';
}

// Application State
const state = {
  isDeckOpen: false,
  activeCassette: 'track_1', 
  isPlaying: false,
  isAnnouncementPlaying: false,
  isChaiPlaying: false,
  customYtId: '',
  fanSpeed: 0, 
  isLightOn: true,
  isShutterClosed: false,
  isWindy: false,
  isRaining: false,
  trainSpeed: 'cruise', 
  timeOfDay: 'day',
  volume: 80,
  tuning: 50,
  isChainPulled: false,
  tapeProgress: 0.2,
  windowCoords: null,
  useSynthFallback: false,
  isAmbienceMuted: false,
  trainType: 'rajdhani',
  activeRoute: 'punjab'
};

// Punjab playlist tracks
const cassetteTracks = {
    "track_1": { title: "DAS MERIYA DILWARAVE WITH LYRICS", ytId: "xiA1D0QEHlQ", color: "#e74c3c" },
    "track_2": { title: "DHOKHA NAHIN KAMAIDA", ytId: "zoi-JS28X_w", color: "#3498db" },
    "track_3": { title: "PEHLE LALKARE NAAL MAIN DAR GAI", ytId: "cUvKUuoVd3E", color: "#f1c40f" },
    "track_4": { title: "CHALLA", ytId: "fsM-eXNNSSo", color: "#2ecc71" },
    "track_5": { title: "GORA GORA RANG", ytId: "cQVStCN0pSc", color: "#9b59b6" },
    "track_6": { title: "HEER", ytId: "ULnhQfu_ZaY", color: "#1abc9c" },
    "track_7": { title: "NACHI JO SADE NAAL", ytId: "GnMDTDAn7XY", color: "#e67e22" },
    "track_8": { title: "PEER TERE JAAN DI", ytId: "CTfqNNiY4RM", color: "#34495e" },
    "track_9": { title: "BABA VE KALA MAROR", ytId: "M0RgRY0QGVs", color: "#e74c3c" },
    "track_10": { title: "BATTUA", ytId: "b_KKY_0WLAI", color: "#3498db" },
    "track_11": { title: "OYE HOYE", ytId: "Bsc3_gm74pQ", color: "#f1c40f" },
    "track_12": { title: "SAJNA TOON [FULL SONG] YAARA O DILDARA", ytId: "cwpvoSkCgAg", color: "#2ecc71" },
    "track_13": { title: "MIRZA", ytId: "WCF2uIszOmM", color: "#9b59b6" },
    "track_14": { title: "YAARA O DILDAARA", ytId: "hFlIJwMr8lI", color: "#1abc9c" },
    "track_15": { title: "LONG GAVAIYAN", ytId: "slHtvkBgncg", color: "#e67e22" },
    "track_16": { title: "ANKHIYANCH NEEDAR", ytId: "cEX2UYm8ZvM", color: "#34495e" },
    "track_17": { title: "LAKH PARDESI", ytId: "HB-UggZklGw", color: "#e74c3c" },
    "track_18": { title: "CHINTA NA KAR YAAR", ytId: "n0wqDc0jwYA", color: "#3498db" },
    "track_19": { title: "SAJNA VE SAJNA", ytId: "U_5QxvdzkjY", color: "#f1c40f" },
    "track_20": { title: "GURDAS MAAN - BOOT POLISHAN", ytId: "vDRijlkhzfI", color: "#2ecc71" },
    "track_21": { title: "MANKE", ytId: "Zc7r96CoVJ0", color: "#9b59b6" },
    "track_22": { title: "MAMLA GARBAR HAI", ytId: "XwyIkqjQLNI", color: "#1abc9c" },
    "track_23": { title: "DIL DA MAMLA HAI", ytId: "oPYOPb5tlzA", color: "#e67e22" },
    "track_24": { title: "RAATI CHANN NAAL GALLAN KARKEY", ytId: "zW5us8JDNlk", color: "#34495e" },
    "track_25": { title: "NEE PUT JATTAN DA", ytId: "cg6tbdMeAeQ", color: "#e74c3c" },
    "track_26": { title: "SUN MERE CHANN MAHIYA - OFFICIAL VIDEO SONG", ytId: "5QaEk3YXMBU", color: "#3498db" },
    "track_27": { title: "MAKHNA", ytId: "7GSTNYxbyEM", color: "#f1c40f" },
    "track_28": { title: "AKHIYAN CH TON WASDA", ytId: "sCBv9tqdVvQ", color: "#2ecc71" },
    "track_29": { title: "DO PALL", ytId: "rdOM4unXcPs", color: "#9b59b6" },
    "track_30": { title: "JOGIYA VE JOGIYA", ytId: "i5cboVTy0uo", color: "#1abc9c" },
    "track_31": { title: "PUNJABI TAPPE", ytId: "9aoBDJ_Ajrg", color: "#e67e22" },
    "track_32": { title: "RUKHAN WANGOO KHADE RAHE", ytId: "q0P3mKHG2ak", color: "#34495e" }
};
// Pick a random track as the default loaded tape on startup
const trackKeys = Object.keys(cassetteTracks).filter(k => k !== 'custom_stream');
const randomKey = trackKeys[Math.floor(Math.random() * trackKeys.length)];
state.activeCassette = randomKey;

// YouTube API variables
let ytPlayer = null;
let ytApiReady = false;

// Define callback before appending the script to prevent race conditions
window.onYouTubeIframeAPIReady = function() {
  const defaultTrack = cassetteTracks[state.activeCassette];
  ytPlayer = new YT.Player('ytAudioPlayer', {
    height: '100%',
    width: '100%',
    videoId: defaultTrack ? defaultTrack.ytId : 'iSUK1QoK9-E',
    playerVars: {
      'playsinline': 1,
      'controls': 0,
      'disablekb': 1,
      'fs': 0,
      'rel': 0,
      'modestbranding': 1,
      'origin': window.location.origin
    },
    events: {
      'onReady': () => {
        ytApiReady = true;
        console.log("YT Player Connected.");
        if (state.playOnReady) {
          state.playOnReady = false;
          playCassette();
        }
      },
      'onStateChange': onPlayerStateChange,
      'onError': (e) => {
        console.warn("YT Embed Player restricted or offline. Swapping to arpeggiator fallback...", e);
        switchToSynthFallback();
      }
    }
  });
};

// Safely inject YouTube IFrame Player API
const tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
document.head.appendChild(tag);

function onPlayerStateChange(e) {
  if (e.data === YT.PlayerState.PLAYING) {
    if (state.activeCassette === 'custom_stream') {
      if (ytPlayer && typeof ytPlayer.getVideoData === 'function') {
        const data = ytPlayer.getVideoData();
        if (data) {
          if (data.title) document.getElementById('playerSongTitle').textContent = data.title;
          if (data.author) document.getElementById('playerSongArtist').textContent = data.author;
          if (data.video_id) {
            const albumArt = document.getElementById('playerAlbumArt');
            if (albumArt) {
              albumArt.innerHTML = `<img src="https://i.ytimg.com/vi/${data.video_id}/hqdefault.jpg" alt="Art" style="width: 100%; height: 100%; object-fit: cover;">`;
            }
          }
        }
      }
    }
  }
  if (e.data === YT.PlayerState.ENDED) {
    if (state.isPlaying) {
      if (state.useSynthFallback) {
        // Sequencer handles loop
      } else {
        ytPlayer.playVideo();
      }
    }
  }
}

function switchToSynthFallback() {
  state.useSynthFallback = true;
  const trackName = state.activeCassette ? cassetteTracks[state.activeCassette].title : "LOFI SYNTH";
  document.getElementById('playerSongTitle').textContent = `SYNTH: ${trackName}`;
  document.getElementById('playerSongArtist').textContent = "Local Web Audio Synth";
  
  const albumArt = document.getElementById('playerAlbumArt');
  if (albumArt) {
    albumArt.textContent = "📀";
  }

  if (state.isPlaying) {
    audio.startSynthTape();
  }
}

// Coordinate Aligner mapping directly on top of premium_coach_layout illustration features
function alignCompartmentElements() {
  const visualsEl = document.getElementById('compartmentVisuals') || document.body;
  const dispWidth = visualsEl.clientWidth;
  const dispHeight = visualsEl.clientHeight;
  const canvas = document.getElementById('cabinCanvas');
  if (!canvas) return;
  
  canvas.width = 1920; 
  canvas.height = 1080;
  
  const ctx = canvas.getContext('2d');
  
  if (!window.cabinImg || !window.cabinImg.complete) return;
  
  const img = window.cabinImg;
  
  ctx.clearRect(0, 0, 1920, 1080);
  ctx.drawImage(img, 0, 0, 1920, 1080);

  // Fit cover scaling calculations
  const scale = Math.max(dispWidth / 1920, dispHeight / 1080);
  document.documentElement.style.setProperty('--cabin-scale', scale);
  
  const renderedWidth = 1920 * scale;
  const renderedHeight = 1080 * scale;
  const offsetX = (dispWidth - renderedWidth) / 2;
  let offsetY = (dispHeight - renderedHeight) / 2;
  if (offsetY < 0) {
    offsetY = offsetY * 0.15;
  }

  canvas.style.position = 'absolute';
  canvas.style.left = `${offsetX}px`;
  canvas.style.top = `${offsetY}px`;
  canvas.style.width = `${renderedWidth}px`;
  canvas.style.height = `${renderedHeight}px`;
  canvas.style.objectFit = 'fill';

  const mapElement = (elId, xPct, yPct, wPct, hPct, isSquare = false, clampToScreen = false) => {
    const el = document.getElementById(elId);
    if (!el) return;
    
    let w = wPct * renderedWidth;
    let h = hPct * renderedHeight;
    if (isSquare) h = w;
    
    let x = offsetX + (xPct * renderedWidth);
    let y = offsetY + (yPct * renderedHeight);
    
    if (clampToScreen) {
      x = Math.max(12, Math.min(dispWidth - w - 12, x));
      y = Math.max(12, Math.min(dispHeight - h - 12, y));
    }
    
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;
    el.style.width = `${w}px`;
    el.style.height = `${h}px`;
    el.style.position = 'absolute';
  };

  // Align UI elements
  mapElement('skyClock', 0.04, 0.035, 0.09, 0.04, false, true);
  mapElement('skyOnlineCounter', 0.86, 0.035, 0.10, 0.04, false, true);
  mapElement('chaiGlass', 0.682, 0.61, 0.07, 0.20); 
  mapElement('diaryHotspot', 0.38, 0.78, 0.30, 0.20); // Diary hotspot over the notebook

  const timeCard = document.getElementById('timeOfDayCard');
  if (timeCard) {
    const w = 0.11 * renderedWidth;
    const h = timeCard.offsetHeight || 300;
    let x = offsetX + (0.04 * renderedWidth);
    let y = offsetY + (0.32 * renderedHeight);
    
    x = Math.max(12, Math.min(dispWidth - w - 12, x));
    y = Math.max(12, Math.min(dispHeight - h - 12, y));
    
    timeCard.style.left = `${x}px`;
    timeCard.style.top = `${y}px`;
    timeCard.style.width = `${w}px`;
    timeCard.style.height = 'auto';
    timeCard.style.position = 'absolute';
  }
}

function processCabinChromaKey() {
  const img = new Image();
  // Force browser cache buster bypass for the image asset
  let imgSrc = '/train_cabin_chromakey.jpg?v=2.0';
  if (state.activeRoute === 'punjab') {
    imgSrc = '/punjab_cabin_chromakey.jpg?v=2.0';
  } else if (state.activeRoute === 'jammu') {
    imgSrc = '/jammu_cabin_chromakey.jpg?v=2.0';
  } else if (state.activeRoute === 'english') {
    imgSrc = '/english_cabin_chromakey.jpg?v=2.0';
  }
  img.src = imgSrc;  
  img.onload = () => {
    window.cabinImg = img;
    alignCompartmentElements();
    window.addEventListener('resize', alignCompartmentElements);
    console.log("Illustration mapping and dynamic resize hook bound.");
  };

  img.onerror = (e) => {
    console.error("Failed to load chromakey cabin layout asset.", e);
  };
}

// Frame ticker
let animationFrameId = null;
function runVisualFrameTicker() {
  audio.tick();

  // Rotate fan blades and apply dynamic motion blur based on speed
  const fanEl = document.getElementById('fanBlades');
  if (fanEl) {
    if (audio.fanSpeedVal > 0.01) {
      if (!state.fanAngle) state.fanAngle = 0;
      state.fanAngle += audio.fanSpeedVal * 8; 
      // Apply rotateX(41deg) to skew rotation into the 3D perspective of the slanted ceiling
      fanEl.style.transform = `rotateX(41deg) rotate(${state.fanAngle}deg)`;
      
      const blurPx = Math.min(2.5, audio.fanSpeedVal * 2.2);
      fanEl.style.setProperty('--fan-blur', `${blurPx}px`);
    } else {
      fanEl.style.setProperty('--fan-blur', '0px');
    }
  }

  // Time-delta normalized animation scrolling to prevent browser keyframe re-evaluation stutters
  const nowTime = performance.now();
  if (!state.lastFrameTime) state.lastFrameTime = nowTime;
  const dt = Math.min(100, nowTime - state.lastFrameTime) / 16.666;
  state.lastFrameTime = nowTime;

  if (!state.scrollOffsets) {
    state.scrollOffsets = { mountains: 0, landscape: 0, telegraph: 0, foreground: 0 };
  }

  if (audio.trainSpeedVal > 0.01 && state.activeRoute === 'hindi') {
    const multiplier = audio.trainSpeedVal * dt;

    // Speeds are calibrated to align exactly with original CSS duration ratios (50s, 22s, 6s, 1.4s)
    state.scrollOffsets.foreground = (state.scrollOffsets.foreground - (0.595 * multiplier)) % 50;
    state.scrollOffsets.telegraph = (state.scrollOffsets.telegraph - (0.139 * multiplier)) % 50;
    state.scrollOffsets.landscape = (state.scrollOffsets.landscape - (0.038 * multiplier)) % 50;
    state.scrollOffsets.mountains = (state.scrollOffsets.mountains - (0.017 * multiplier)) % 50;

    const layerM = document.getElementById('layerMountains');
    const layerL = document.getElementById('layerLandscape');
    const layerT = document.getElementById('layerTelegraph');
    const layerF = document.getElementById('layerForeground');

    if (layerM) layerM.style.transform = `translate3d(${state.scrollOffsets.mountains}%, 0, 0)`;
    if (layerL) layerL.style.transform = `translate3d(${state.scrollOffsets.landscape}%, 0, 0)`;
    if (layerT) layerT.style.transform = `translate3d(${state.scrollOffsets.telegraph}%, 0, 0)`;
  } else if (state.activeRoute !== 'hindi') {
    state.scrollOffsets = { mountains: 0, landscape: 0, telegraph: 0, foreground: 0 };
    const layerM = document.getElementById('layerMountains');
    const layerL = document.getElementById('layerLandscape');
    const layerT = document.getElementById('layerTelegraph');
    if (layerM) layerM.style.transform = `translate3d(0, 0, 0)`;
    if (layerL) layerL.style.transform = `translate3d(0, 0, 0)`;
    if (layerT) layerT.style.transform = `translate3d(0, 0, 0)`;
  }

  // Spawn visual rain splashes on the window glass pane
  if (state.isRaining && Math.random() < 0.15) {
    const viewport = document.getElementById('windowViewport');
    if (viewport) {
      const splash = document.createElement('div');
      splash.className = 'rain-splash';
      
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      splash.style.left = `${x}%`;
      splash.style.top = `${y}%`;
      
      const size = 10 + Math.random() * 14; // 10px to 24px (Larger, more visible)
      splash.style.width = `${size}px`;
      splash.style.height = `${size * 0.5}px`; // Squashed ellipse matching perspective
      
      viewport.appendChild(splash);
      setTimeout(() => splash.remove(), 380);
    }
  }

  // Spawn visual wind particles (leaves & gusts) blowing across the window viewport
  if (state.isWindy && Math.random() < 0.09) {
    const viewport = document.getElementById('windowViewport');
    if (viewport) {
      const isLeaf = Math.random() < 0.45;
      const item = document.createElement('div');
      item.className = isLeaf ? 'wind-particle' : 'wind-streak';
      
      const y = 10 + Math.random() * 75; // Confined vertically to window window bounds
      item.style.top = `${y}%`;
      item.style.left = '100%';
      
      if (isLeaf) {
        const size = 6 + Math.random() * 8; // 6px to 14px
        item.style.width = `${size}px`;
        item.style.height = `${size * 0.7}px`;
        
        // Random cozy leaf colors (rust gold, deep orange, moss green)
        const colors = ['#c0392b', '#d35400', '#27ae60', '#f1c40f'];
        item.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
      } else {
        const width = 40 + Math.random() * 50; // 40px to 90px
        item.style.width = `${width}px`;
      }
      
      viewport.appendChild(item);
      const duration = isLeaf ? 850 : 550;
      setTimeout(() => item.remove(), duration);
    }
  }

  // Rotate Spotify player vinyl disk art
  const albumArt = document.getElementById('playerAlbumArt');
  if (albumArt && state.isPlaying) {
    if (!state.artRotation) state.artRotation = 0;
    state.artRotation += 1.5;
    albumArt.style.transform = `rotate(${state.artRotation}deg)`;
  }

  // Update progress bar and duration label
  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  if (state.isPlaying) {
    if (ytPlayer && ytApiReady && !state.useSynthFallback && typeof ytPlayer.getCurrentTime === 'function') {
      const current = ytPlayer.getCurrentTime() || 0;
      const duration = ytPlayer.getDuration() || 0;
      document.getElementById('timeElapsed').textContent = formatTime(current);
      document.getElementById('timeTotal').textContent = duration > 0 ? formatTime(duration) : '--:--';
      
      const pct = duration > 0 ? (current / duration) * 100 : 0;
      document.getElementById('progressBarFill').style.width = `${pct}%`;
    } else {
      // Synth fallback progress simulation
      state.tapeProgress += 0.00015;
      if (state.tapeProgress > 0.99) state.tapeProgress = 0.01;
      
      document.getElementById('timeElapsed').textContent = formatTime(state.tapeProgress * 210);
      document.getElementById('timeTotal').textContent = '3:30';
      document.getElementById('progressBarFill').style.width = `${state.tapeProgress * 100}%`;
    }
  }

  // Update VU needles
  updateVUNeedles();

  animationFrameId = requestAnimationFrame(runVisualFrameTicker);
}

// Needle updates
let targetNeedleL = -45;
let targetNeedleR = -45;
let currentNeedleL = -45;
let currentNeedleR = -45;

function updateVUNeedles() {
  if (state.isPlaying) {
    const deviation = Math.abs(50 - state.tuning) / 50;
    const signalFactor = (state.volume / 100) * (1 - deviation * 0.85);
    const staticJitter = deviation * 15;

    const beatStrength = Math.random() > 0.85 ? 40 : (Math.random() * 15);
    const audioPeakL = (beatStrength * signalFactor) + (Math.random() * staticJitter);
    const audioPeakR = (beatStrength * signalFactor * 0.95) + (Math.random() * staticJitter);

    targetNeedleL = -45 + audioPeakL * 1.6;
    targetNeedleR = -45 + audioPeakR * 1.6;
  } else {
    targetNeedleL = -45;
    targetNeedleR = -45;
  }

  const lDiff = targetNeedleL - currentNeedleL;
  currentNeedleL += lDiff * (lDiff > 0 ? 0.3 : 0.08); 

  const rDiff = targetNeedleR - currentNeedleR;
  currentNeedleR += rDiff * (rDiff > 0 ? 0.3 : 0.08);

  currentNeedleL = Math.max(-45, Math.min(45, currentNeedleL));
  currentNeedleR = Math.max(-45, Math.min(45, currentNeedleR));

  document.documentElement.style.setProperty('--needle-l-rot', `${currentNeedleL}deg`);
  document.documentElement.style.setProperty('--needle-r-rot', `${currentNeedleR}deg`);
}

// Init Setup
document.addEventListener("DOMContentLoaded", () => {
  // Polyfill ID mismatches between Train page and Room pages
  const mapId = (targetId, fallbackId) => {
    const el = document.getElementById(fallbackId);
    if (el && !document.getElementById(targetId)) {
      el.id = targetId;
    }
  };
  mapId('progressBarBg', 'progressBg');
  mapId('progressBarFill', 'progressFill');
  mapId('timeElapsed', 'timeCurrent');
  mapId('btnPlaylistSelect', 'playlistTrigger');

  // Set initial route styling on load
  const initialRoute = state.activeRoute;
  document.body.classList.remove('route-hindi', 'route-punjab', 'route-jammu', 'route-english');
  document.body.classList.add(`route-${initialRoute}`);

  processCabinChromaKey();

  // Mobile tab navigation handler
  const tabButtons = document.querySelectorAll('.tab-nav-btn');
  const panelsContainer = document.getElementById('compartmentPanels');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const tab = e.currentTarget.getAttribute('data-tab');
      if (panelsContainer) {
        panelsContainer.className = `compartment-panels active-tab-${tab}`;
      }
      tabButtons.forEach(b => b.classList.toggle('active', b === e.currentTarget));
    });
  });
  setupDraggableShutters();
  setupEmergencyChain();
  setupRotaryControls();
  setupInteractiveToggles();
  setupFloatingDust();
  // Dynamically render menu items
  rebuildPlaylistMenu();
  // Set initial player details from the randomized default active cassette
  const defaultTrack = cassetteTracks[state.activeCassette];
  if (defaultTrack) {
    document.getElementById('playerSongTitle').textContent = defaultTrack.title;
    const albumArt = document.getElementById('playerAlbumArt');
    if (albumArt && defaultTrack.ytId) {
      albumArt.innerHTML = `<img src="https://i.ytimg.com/vi/${defaultTrack.ytId}/hqdefault.jpg" alt="Art" style="width: 100%; height: 100%; object-fit: cover;">`;
    }
  }

  // Spotify Glass player bindings
  const btnPlayPause = document.getElementById('btnPlayPause');
  const playlistMenu = document.getElementById('playlistMenu');
  const btnPlaylistSelect = document.getElementById('btnPlaylistSelect') || document.getElementById('playlistTrigger');
  const bplTapeDeck = document.getElementById('bplTapeDeck');

  btnPlayPause.addEventListener('click', () => {
    if (!state.activeCassette) {
      const defaultTrack = cassetteTracks[state.activeCassette] || { ytId: 'iSUK1QoK9-E' };
      loadCassette(state.activeCassette || 'track_1', defaultTrack.ytId);
      return;
    }
    if (state.isPlaying) pauseCassette();
    else playCassette();
  });

  if (btnPlaylistSelect) btnPlaylistSelect.addEventListener('click', (e) => {
    e.stopPropagation();
    playlistMenu.classList.toggle('open');
  });

  // Clicking the illustrated tape deck on the table is a shortcut that opens the menu!
  if (bplTapeDeck) bplTapeDeck.addEventListener('click', (e) => {
    e.stopPropagation();
    playlistMenu.classList.toggle('open');
    // Highlight the table tape deck with a brief outline flash
    bplTapeDeck.style.outline = "3px dashed #fff";
    setTimeout(() => { bplTapeDeck.style.outline = ""; }, 300);
  });

  // Prev / Next tape selectors
  document.getElementById('btnNext').addEventListener('click', playNextTape);
  document.getElementById('btnPrev').addEventListener('click', playPrevTape);

  // Close dropdown on click outside
  document.addEventListener('click', () => {
    playlistMenu.classList.remove('open');
  });

  // Playlist dropdown menu selection (uses delegation for dynamic items)
  playlistMenu.addEventListener('click', (e) => {
    const menuItem = e.target.closest('.menu-item');
    if (!menuItem) return;
    
    e.stopPropagation();
    const id = menuItem.getAttribute('data-id');
    const ytId = menuItem.getAttribute('data-youtube');
    
    if (id === 'custom_stream') {
      const form = document.getElementById('customTapeForm');
      form.style.display = form.style.display === 'none' ? 'block' : 'none';
    } else {
      playlistMenu.classList.remove('open');
      loadCassette(id, ytId);
    }
  });

  function extractYoutubeId(url) {
    if (!url) return null;
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/|music.youtube.com\/watch\?v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  }

  // Custom tape loader button
  const btnLoadCustomTape = document.getElementById('btnLoadCustomTape');
  if (btnLoadCustomTape) {
    btnLoadCustomTape.addEventListener('click', (e) => {
      e.stopPropagation();
      const inputVal = document.getElementById('ytUrlInput').value.trim();
      const ytId = extractYoutubeId(inputVal) || inputVal;

      if (ytId) {
        playlistMenu.classList.remove('open');
        const customTapeForm = document.getElementById('customTapeForm');
        if (customTapeForm) customTapeForm.style.display = 'none';
        loadCassette('custom_stream', ytId);
      } else {
        alert("Invalid Youtube link or ID!");
      }
    });
  }

  // Volume slider
  document.getElementById('spotifyVolumeSlider').addEventListener('input', (e) => {
    state.volume = parseInt(e.target.value);
    updateAudioVolumes();
    const volIcon = document.getElementById('volIcon');
    if (state.volume === 0) volIcon.textContent = "🔇";
    else if (state.volume < 40) volIcon.textContent = "🔈";
    else volIcon.textContent = "🔊";
  });

  // Seeking on progress bar
  document.getElementById('progressBarBg').addEventListener('click', (e) => {
    if (!ytPlayer || !ytApiReady || !state.activeCassette || state.useSynthFallback) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const width = rect.width;
    const pct = Math.max(0, Math.min(1, clickX / width));
    
    if (typeof ytPlayer.getDuration === 'function') {
      const duration = ytPlayer.getDuration();
      if (duration > 0) {
        ytPlayer.seekTo(pct * duration, true);
      }
    }
  });

  // Train selector rotary dial and label bindings
  const trainDial = document.getElementById('trainDial');
  if (trainDial) {
    trainDial.addEventListener('click', () => {
      const types = ['rajdhani', 'passenger', 'steam', 'goods'];
      let idx = types.indexOf(state.trainType);
      idx = (idx + 1) % types.length;
      setTrainType(types[idx]);
    });
  }

  document.querySelectorAll('.train-label').forEach(lbl => {
    lbl.addEventListener('click', (e) => {
      const type = e.target.getAttribute('data-type');
      setTrainType(type);
    });
  });
  setupSoundboardTriggers();
  setupKeyboardShortcuts();
  runVisualFrameTicker();
  startSkyClock();
  startSkyOnlineCounter();
  document.body.addEventListener('click', () => {
    if (!audio.initialized) {
      audio.init();
    }
    audio.resume();
  }, { once: true });
});

// Floating dust generator
function setupFloatingDust() {
  const container = document.getElementById('dustContainer');
  if (!container) return;
  const particleCount = 20;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.className = 'dust-particle';
    particle.style.left = `${Math.random() * 90 + 5}%`;
    particle.style.animationDelay = `${Math.random() * 12}s`;
    particle.style.animationDuration = `${10 + Math.random() * 10}s`;
    container.appendChild(particle);
  }
}

function setupDraggableShutters() {
  const windowFrame = document.getElementById('windowViewport');
  
  if (windowFrame) {
    // Intercept and cancel any wheel scroll attempts directly on the window viewport
    windowFrame.addEventListener('wheel', (e) => {
      e.preventDefault();
    }, { passive: false });
    
    // Intercept and cancel scrollable touchmove events inside the window viewport
    windowFrame.addEventListener('touchmove', (e) => {
      if (!e.target.closest('.shutter-handle')) {
        e.preventDefault();
      }
    }, { passive: false });

    windowFrame.addEventListener('scroll', () => {
      windowFrame.scrollTop = 0;
      windowFrame.scrollLeft = 0;
    });
  }

  window.windowShutters = [
    { el: document.getElementById('shutterGlass'), handle: document.querySelector('.glass-handle'), currY: -76 },
    { el: document.getElementById('shutterMetal'), handle: document.querySelector('.metal-handle'), currY: -76 }
  ].filter(shutter => shutter.el && shutter.handle);

  window.windowShutters.forEach(shutter => {
    let startY = 0;
    let startVal = shutter.currY;

    // Force initial placement inline to override any cached CSS style values
    shutter.el.style.transform = `translateY(${shutter.currY}%)`;

    const onPointerDown = (e) => {
      e.preventDefault();
      startY = e.clientY || e.touches[0].clientY;
      startVal = shutter.currY;

      // Disable transition animations during manual dragging to avoid lag/flicker
      shutter.el.style.transition = 'none';

      document.addEventListener('mousemove', onPointerMove);
      document.addEventListener('touchmove', onPointerMove, { passive: false });
      document.addEventListener('mouseup', onPointerUp);
      document.addEventListener('touchend', onPointerUp);
      
      shutter.handle.style.background = '#e2b865'; 
    };

    const onPointerMove = (e) => {
      const currentY = e.clientY || e.touches[0].clientY;
      const deltaY = currentY - startY;
      const height = windowFrame.clientHeight;
      const percent = (deltaY / height) * 100;

      let newY = startVal + percent;
      newY = Math.max(-76, Math.min(-8, newY)); 
      
      shutter.currY = newY;
      shutter.el.style.transform = `translateY(${newY}%)`;

      // Real-time synchronization with the digital switchboard console button
      const shutterInd = document.getElementById('shutterToggleIndicator');
      if (shutterInd) {
        state.isShutterClosed = (newY > -42); // If dragged halfway closed, mark as closed
        shutterInd.classList.toggle('active', state.isShutterClosed);
      }

      updateAmbientDarkness();
    };

    const onPointerUp = () => {
      document.removeEventListener('mousemove', onPointerMove);
      document.removeEventListener('touchmove', onPointerMove);
      document.removeEventListener('mouseup', onPointerUp);
      document.removeEventListener('touchend', onPointerUp);

      shutter.handle.style.background = ''; 

      // Slam contact sound clink if limits are reached
      if (shutter.currY === -8 || shutter.currY === -76) {
        audio.playShutterClink();
      }
    };

    shutter.handle.addEventListener('mousedown', onPointerDown);
    shutter.handle.addEventListener('touchstart', onPointerDown, { passive: false });
  });
}

// Emergency Chain
function setupEmergencyChain() {
  const chainPull = document.getElementById('chainPull');
  if (!chainPull) return;
  let startY = 0;
  let isDragging = false;

  const onStart = (e) => {
    if (state.isChainPulled) return;
    isDragging = true;
    startY = e.clientY || e.touches[0].clientY;
    chainPull.classList.add('pulled');

    document.addEventListener('mousemove', onMove);
    document.addEventListener('touchmove', onMove, { passive: false });
    document.addEventListener('mouseup', onEnd);
    document.addEventListener('touchend', onEnd);
  };

  const onMove = (e) => {
    if (!isDragging) return;
    const currentY = e.clientY || e.touches[0].clientY;
    const deltaY = currentY - startY;

    if (deltaY > 25) {
      triggerBrakesSequence();
      onEnd();
    }
  };

  const onEnd = () => {
    isDragging = false;
    chainPull.classList.remove('pulled');
    document.removeEventListener('mousemove', onMove);
    document.removeEventListener('touchmove', onMove);
    document.removeEventListener('mouseup', onEnd);
    document.removeEventListener('touchend', onEnd);
  };

  chainPull.addEventListener('mousedown', onStart);
  chainPull.addEventListener('touchstart', onStart, { passive: false });
}

function triggerBrakesSequence() {
  if (state.isChainPulled) return;
  state.isChainPulled = true;

  audio.playEmergencyBrakeScreech();

  const frame = document.getElementById('compartment');
  frame.style.animation = 'brakeJolt 0.5s infinite alternate';

  let count = 0;
  const warningFlash = setInterval(() => {
    const ambient = document.getElementById('ambientOverlay');
    ambient.style.background = count % 2 === 0 ? 'rgba(231, 76, 60, 0.45)' : 'rgba(0, 0, 0, 0.8)';
    ambient.style.mixBlendMode = 'multiply';
    count++;
    if (count > 5) {
      clearInterval(warningFlash);
      frame.style.animation = ''; 
      setTrainSpeed('stop');
      updateAmbientDarkness();
    }
  }, 400);

  // Randomized stop duration between 5 and 10 seconds
  const stopDurationMs = (5 + Math.random() * 5) * 1000;
  
  // Play warning horn 1.8 seconds before train departures
  setTimeout(() => {
    const horn = audio.playHorn();
    setTimeout(() => horn.stop(), 2000);
  }, 2400 + stopDurationMs - 1800);

  // Accelerate to slow after the randomized stop duration ends
  setTimeout(() => {
    setTrainSpeed('slow');
    setTimeout(() => {
      setTrainSpeed('cruise');
      state.isChainPulled = false;
    }, 3000);
  }, 2400 + stopDurationMs);
}

// Rotary controls drag interactions (knob rotations mapped visually over illustrated knobs)
function setupRotaryControls() {
  const volKnob = document.getElementById('volKnob');
  const tuneKnob = document.getElementById('tuneKnob');
  if (!volKnob || !tuneKnob) return; 

  const controls = [
    { knob: volKnob, min: 0, max: 100, curr: 80, onUpdate: (v) => { state.volume = v; updateAudioVolumes(); } },
    { knob: tuneKnob, min: 0, max: 100, curr: 50, onUpdate: (v) => { state.tuning = v; updateRadioTuningQuality(); } }
  ];

  controls.forEach(ctrl => {
    let startY = 0;
    let startVal = ctrl.curr;

    const onPointerDown = (e) => {
      e.preventDefault();
      startY = e.clientY || e.touches[0].clientY;
      startVal = ctrl.curr;

      document.addEventListener('mousemove', onPointerMove);
      document.addEventListener('touchmove', onPointerMove, { passive: false });
      document.addEventListener('mouseup', onPointerUp);
      document.addEventListener('touchend', onPointerUp);
    };

    const onPointerMove = (e) => {
      const currentY = e.clientY || e.touches[0].clientY;
      const deltaY = startY - currentY; 
      
      let newVal = startVal + (deltaY * 0.6); 
      newVal = Math.max(ctrl.min, Math.min(ctrl.max, newVal));
      ctrl.curr = Math.round(newVal);

      // Rotate transparent pointer highlight
      const angle = -135 + (ctrl.curr / (ctrl.max - ctrl.min)) * 270;
      ctrl.knob.style.transform = `rotate(${angle}deg)`;

      if (ctrl.knob.id === 'tuneKnob') {
        const mhz = (88.0 + (ctrl.curr / 100) * 20).toFixed(1);
        document.getElementById('deckScreen').textContent = `FM: ${mhz} MHz`;
      } else {
        document.getElementById('deckScreen').textContent = `VOL: ${ctrl.curr}%`;
      }

      ctrl.onUpdate(ctrl.curr);
    };

    const onPointerUp = () => {
      document.removeEventListener('mousemove', onPointerMove);
      document.removeEventListener('touchmove', onPointerMove);
      document.removeEventListener('mouseup', onPointerUp);
      document.removeEventListener('touchend', onPointerUp);
      
      // Restore default deck screen content
      setTimeout(() => {
        if (state.isPlaying) {
          const name = cassetteTracks[state.activeCassette].title;
          document.getElementById('deckScreen').textContent = state.useSynthFallback ? `SYNTH: ${name}` : name;
        } else {
          document.getElementById('deckScreen').textContent = state.activeCassette ? "TAPE LOADED" : "NO TAPE";
        }
      }, 1000);
    };

    ctrl.knob.addEventListener('mousedown', onPointerDown);
    ctrl.knob.addEventListener('touchstart', onPointerDown, { passive: false });
  });
}

function setTrainSpeed(speed) {
  state.trainSpeed = speed;
  const velocities = [0.0, 0.35, 1.0, 1.6];
  const index = ['stop', 'slow', 'cruise', 'express'].indexOf(speed);
  audio.targetTrainSpeedVal = velocities[index];

  const screen = document.getElementById('deckScreen');
  if (speed === 'stop') {
    screen.textContent = state.isPlaying ? cassetteTracks[state.activeCassette].title : "STATION HALT";
  } else {
    if (state.isPlaying) {
      screen.textContent = cassetteTracks[state.activeCassette].title;
    } else {
      screen.textContent = "TRAIN CHUGGING";
    }
  }
}
function rebuildPlaylistMenu() {
  const dynamicMenuItems = document.getElementById('dynamicMenuItems');
  if (!dynamicMenuItems) return;
  
  dynamicMenuItems.innerHTML = '';
  
  Object.keys(cassetteTracks).forEach(key => {
    if (key === 'custom_stream') return;
    const track = cassetteTracks[key];
    const item = document.createElement('div');
    item.className = 'menu-item';
    item.setAttribute('data-id', key);
    item.setAttribute('data-youtube', track.ytId);
    
    if (state.activeCassette === key) {
      item.classList.add('active');
    }
    
    const cleanTitle = track.title.toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
    
    item.innerHTML = `
      <span class="item-color-dot" style="background: ${track.color || '#e2b865'};"></span>
      <span class="item-title">${cleanTitle}</span>
    `;
    dynamicMenuItems.appendChild(item);
  });
}

function setupInteractiveToggles() {
  const btnLight = document.getElementById('btnLight') || document.getElementById('btnCabinLight');
  const btnFan = document.getElementById('btnFan');
  const btnWind = document.getElementById('btnWind');
  const btnRain = document.getElementById('btnRain');
  const btnShutter = document.getElementById('btnShutter');

  const lightInd = document.getElementById('lightToggleIndicator');
  const fanInd = document.getElementById('fanToggleIndicator');
  const windInd = document.getElementById('windToggleIndicator');
  const rainInd = document.getElementById('rainToggleIndicator');
  const shutterInd = document.getElementById('shutterToggleIndicator');

  // Set initial glass toggle positions based on state
  if (lightInd) lightInd.classList.toggle('active', state.isLightOn);
  if (fanInd) fanInd.classList.toggle('active', state.fanSpeed > 0);
  if (windInd) windInd.classList.toggle('active', state.isWindy);
  if (rainInd) rainInd.classList.toggle('active', state.isRaining);
  if (shutterInd) shutterInd.classList.toggle('active', state.isShutterClosed);

  if (btnLight) btnLight.addEventListener('click', () => {
    state.isLightOn = !state.isLightOn;
    audio.playSwitchClick();

    if (lightInd) lightInd.classList.toggle('active', state.isLightOn);
    document.getElementById('compartment').classList.toggle('light-on', state.isLightOn);
    updateAmbientDarkness(); // Update lighting layout immediately!
  });

  if (btnFan) btnFan.addEventListener('click', () => {
    audio.playSwitchClick();
    state.fanSpeed = state.fanSpeed === 0 ? 3 : 0; 

    const isFanActive = state.fanSpeed > 0;
    if (fanInd) fanInd.classList.toggle('active', isFanActive);
    audio.targetFanSpeedVal = isFanActive ? 1.0 : 0.0;
  });

  if (btnWind) btnWind.addEventListener('click', () => {
    state.isWindy = !state.isWindy;
    audio.playSwitchClick();

    if (windInd) windInd.classList.toggle('active', state.isWindy);
  });

  if (btnRain) btnRain.addEventListener('click', () => {
    state.isRaining = !state.isRaining;
    audio.playSwitchClick();

    if (rainInd) rainInd.classList.toggle('active', state.isRaining);
    
    const viewport = document.getElementById('windowViewport');
    if (viewport) viewport.classList.toggle('rain-on', state.isRaining);
  });

  if (btnShutter) btnShutter.addEventListener('click', () => {
    state.isShutterClosed = !state.isShutterClosed;
    audio.playSwitchClick();
    audio.playShutterClink();

    if (shutterInd) shutterInd.classList.toggle('active', state.isShutterClosed);

    const targetY = state.isShutterClosed ? -8 : -76;
    if (window.windowShutters) {
      window.windowShutters.forEach(shutter => {
        shutter.currY = targetY;
        shutter.el.style.transition = 'transform 0.6s cubic-bezier(0.19, 1, 0.22, 1)';
        shutter.el.style.transform = `translateY(${targetY}%)`;
      });
    }

    updateAmbientDarkness();
  });

  const btnFullscreen = document.getElementById('btnFullscreen');
  const fullscreenInd = document.getElementById('fullscreenToggleIndicator');

  const syncFullscreenUI = () => {
    const isFS = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
    const isPseudoFS = document.body.classList.contains('pseudo-fullscreen');
    const isActive = isFS || isPseudoFS;
    
    document.body.classList.toggle('fullscreen-active', isActive);
    
    let exitBtn = document.getElementById('exitFullscreenBtn');
    if (isActive) {
      if (!exitBtn) {
        exitBtn = document.createElement('button');
        exitBtn.id = 'exitFullscreenBtn';
        exitBtn.className = 'exit-fullscreen-btn';
        exitBtn.innerHTML = 'Exit Full Screen ✕';
        document.body.appendChild(exitBtn);
        exitBtn.addEventListener('click', () => {
          if (document.fullscreenElement || document.webkitFullscreenElement) {
            if (document.exitFullscreen) document.exitFullscreen();
            else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
          } else {
            document.body.classList.remove('pseudo-fullscreen');
            syncFullscreenUI();
          }
        });
      }
    } else {
      if (exitBtn) {
        exitBtn.remove();
      }
    }

    if (fullscreenInd) {
      fullscreenInd.classList.toggle('active', isActive);
    }

    setTimeout(() => {
      if (typeof alignCompartmentElements === 'function') {
        alignCompartmentElements();
      }
    }, 100);
  };

  if (btnFullscreen) {
    btnFullscreen.addEventListener('click', () => {
      audio.playSwitchClick();
      const docEl = document.documentElement;
      const nativeFullscreenSupported = !!(docEl.requestFullscreen || docEl.webkitRequestFullscreen || docEl.mozRequestFullScreen || docEl.msRequestFullscreen);

      if (nativeFullscreenSupported) {
        const isFS = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
        if (!isFS) {
          if (docEl.requestFullscreen) {
            docEl.requestFullscreen();
          } else if (docEl.webkitRequestFullscreen) {
            docEl.webkitRequestFullscreen();
          } else if (docEl.mozRequestFullScreen) {
            docEl.mozRequestFullScreen();
          } else if (docEl.msRequestFullscreen) {
            docEl.msRequestFullscreen();
          }
        } else {
          if (document.exitFullscreen) {
            document.exitFullscreen();
          } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
          } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
          }
        }
      } else {
        // Fallback for iOS/iPhone Safari which does not support requestFullscreen on standard elements
        document.body.classList.toggle('pseudo-fullscreen');
        syncFullscreenUI();
      }
    });

    document.addEventListener('fullscreenchange', syncFullscreenUI);
    document.addEventListener('webkitfullscreenchange', syncFullscreenUI);
    document.addEventListener('mozfullscreenchange', syncFullscreenUI);
    document.addEventListener('MSFullscreenChange', syncFullscreenUI);
  }

  document.querySelectorAll('.time-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      audio.playSwitchClick();
      const time = e.target.getAttribute('data-time');
      state.timeOfDay = time;
      
      document.querySelectorAll('.time-btn').forEach(b => b.classList.toggle('active', b === e.target));
      document.body.classList.remove('theme-morning', 'theme-day', 'theme-sunset', 'theme-night');
      document.body.classList.add(`theme-${time}`);
      updateAmbientDarkness();
    });
  });

  // Journey Route Selector
  const btnRouteDropdown = document.getElementById('btnRouteDropdown');
  const routeDropdownMenu = document.getElementById('routeDropdownMenu');
  if (btnRouteDropdown && routeDropdownMenu) {
    btnRouteDropdown.addEventListener('click', (e) => {
      e.stopPropagation();
      routeDropdownMenu.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.route-dropdown-container')) {
        routeDropdownMenu.classList.remove('open');
      }
    });
  }
}

function updateAmbientDarkness() {
  const metalShutter = document.getElementById('shutterMetal');
  if (!metalShutter) return;
  const metalShutterY = parseFloat(metalShutter.style.transform.replace(/[^\d.-]/g, '')) || -76;
  const closedRatio = Math.min(1.0, Math.max(0.0, (metalShutterY + 76) / (76 - 8)));

  const ambient = document.getElementById('ambientOverlay');
  if (!ambient) return;
  
  if (state.timeOfDay === 'morning') {
    const baseShadow = state.isLightOn ? 0.0 : 0.10;
    // Closing the shutter makes the morning light fade out
    const maxDark = state.isLightOn ? 0.68 : 0.88;
    const finalOpacity = (0.08 * (1 - closedRatio)) + baseShadow + closedRatio * (maxDark - baseShadow);
    ambient.style.background = `rgba(255, 218, 119, ${finalOpacity})`;
    ambient.style.mixBlendMode = 'color-burn';
  } else if (state.timeOfDay === 'day') {
    // If lights are on: base shadow is 0. If lights are off: base shadow is 0.12 (gives immediate daylight feedback!)
    const baseShadow = state.isLightOn ? 0.0 : 0.12;
    // Closing the shutter makes the room significantly dark (maxDark of 0.65 or 0.85)
    const maxDark = state.isLightOn ? 0.65 : 0.85;
    const finalOpacity = baseShadow + closedRatio * (maxDark - baseShadow);
    ambient.style.background = `rgba(0, 0, 0, ${finalOpacity})`;
    ambient.style.mixBlendMode = 'multiply';
  } else if (state.timeOfDay === 'sunset') {
    const baseShadow = state.isLightOn ? 0.0 : 0.16;
    // Closing the shutter makes the sunset twilight deep and dark
    const maxDark = state.isLightOn ? 0.72 : 0.90;
    const finalOpacity = (0.14 * (1 - closedRatio)) + baseShadow + closedRatio * (maxDark - baseShadow);
    ambient.style.background = `rgba(243, 104, 33, ${finalOpacity})`;
    ambient.style.mixBlendMode = 'color-burn';
  } else {
    // Night Mode:
    // If light is ON: Cabin is visible with soft night illumination (gets darker when shutter closes)
    // If light is OFF: Cabin is plunged into dark night (nearly pitch black, up to 98% when shutter closes)
    const darkLevel = state.isLightOn ? (0.42 + closedRatio * 0.38) : (0.94 + closedRatio * 0.04);
    ambient.style.background = `rgba(2, 4, 10, ${darkLevel})`;
    ambient.style.mixBlendMode = 'multiply';
  }
}

// Soundboard triggers
function setupSoundboardTriggers() {
  let activeHorn = null;
  const btnHorn = document.getElementById('btnHorn');

  const startHorn = (e) => {
    e.preventDefault();
    if (!activeHorn) {
      activeHorn = audio.playHorn();
      btnHorn.classList.add('active');
    }
  };
  const stopHorn = () => {
    if (activeHorn) {
      activeHorn.stop();
      activeHorn = null;
      btnHorn.classList.remove('active');
    }
  };

  if (btnHorn) btnHorn.addEventListener('mousedown', startHorn);
  if (btnHorn) btnHorn.addEventListener('touchstart', startHorn);
  document.addEventListener('mouseup', stopHorn);
  document.addEventListener('touchend', stopHorn);

  const btnMute = document.getElementById('btnMuteAmbience');
  if (btnMute) btnMute.addEventListener('click', () => {
    state.isAmbienceMuted = !state.isAmbienceMuted;
    audio.playSwitchClick();
    
    const btn = document.getElementById('btnMuteAmbience');
    if (state.isAmbienceMuted) {
      btn.textContent = "🔊 UNMUTE AMBIENCE";
      btn.classList.add('active');
    } else {
      btn.textContent = "🔇 MUTE AMBIENCE";
      btn.classList.remove('active');
    }

    // Sync volume of actively playing soundboard clips immediately
    if (window.announceAudio) {
      window.announceAudio.volume = state.isAmbienceMuted ? 0 : (state.volume / 100) * 0.95 * (state.isLightOn ? 1.0 : 0.45);
    }
    if (window.chaiAudio) {
      window.chaiAudio.volume = state.isAmbienceMuted ? 0 : (state.volume / 100) * 0.95;
    }
  });

  const btnChai = document.getElementById('btnChai');
  if (btnChai) btnChai.addEventListener('click', callChaiWallahVoice);
  const btnAnn = document.getElementById('btnAnnounce'); if (btnAnn) btnAnn.addEventListener('click', playIndianRailwayAnnouncements);

  // Zoomable Ticket interaction
  const ticket = document.getElementById('clampedTicket');
  if (ticket) ticket.addEventListener('click', (e) => {
    // Avoid double close triggers
    if (e.target.id === 'ticketZoomCard' || e.target.closest('#ticketZoomCard')) {
      ticket.classList.remove('zoomed');
      e.stopPropagation();
    } else {
      ticket.classList.add('zoomed');
    }
  });


  // Diary/Notebook interaction
  const diaryHotspot = document.getElementById('diaryHotspot');
  const diaryZoomCard = document.getElementById('diaryZoomCard');
  const closeDiary = document.getElementById('closeDiary');

  if (diaryHotspot && diaryZoomCard) {
    diaryHotspot.addEventListener('click', (e) => {
      e.stopPropagation();
      diaryZoomCard.classList.add('open');
      if (!audio.initialized) audio.init();
      audio.resume();
      audio.playSwitchClick();
    });
  }

  if (closeDiary && diaryZoomCard) {
    closeDiary.addEventListener('click', (e) => {
      e.stopPropagation();
      diaryZoomCard.classList.remove('open');
      audio.playSwitchClick();
    });
  }

  document.addEventListener('click', (e) => {
    if (diaryZoomCard && diaryZoomCard.classList.contains('open')) {
      if (!e.target.closest('#diaryZoomCard') && e.target !== diaryHotspot) {
        diaryZoomCard.classList.remove('open');
      }
    }
  });

  // Tea cup clinking & gulping sounds
  document.getElementById('chaiGlass').addEventListener('click', () => {
    if (!audio.initialized) audio.init();
    audio.resume();

    const now = audio.ctx.currentTime;
    
    // Gulp sound
    const osc = audio.ctx.createOscillator();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(140, now);
    osc.frequency.exponentialRampToValueAtTime(320, now + 0.25);
    const gain = audio.ctx.createGain();
    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
    osc.connect(gain);
    gain.connect(audio.masterGain);
    
    osc.start();
    osc.stop(now + 0.3);

    // Dynamic tea glass clink
    const playGlassClink = (freq, delay) => {
      const clinkOsc = audio.ctx.createOscillator();
      const clinkGain = audio.ctx.createGain();
      clinkOsc.type = 'sine';
      clinkOsc.frequency.setValueAtTime(freq, now + delay);
      
      clinkGain.gain.setValueAtTime(0, now + delay);
      clinkGain.gain.linearRampToValueAtTime(0.08, now + delay + 0.01);
      clinkGain.gain.exponentialRampToValueAtTime(0.0001, now + delay + 0.5);
      
      clinkOsc.connect(clinkGain);
      clinkGain.connect(audio.masterGain);
      
      clinkOsc.start(now + delay);
      clinkOsc.stop(now + delay + 0.6);
    };

    playGlassClink(2800, 0.05); 
    playGlassClink(3400, 0.12);

    alert("Ah! Fresh cardamom tea from a clay-glass.");
  });
}

function updateAudioVolumes() {
  if (ytPlayer && ytApiReady && typeof ytPlayer.setVolume === 'function') {
    const deviation = Math.abs(50 - state.tuning) / 50;
    const finalVol = Math.max(0, state.volume * (1 - deviation));
    ytPlayer.setVolume(finalVol);
  }
}

function updateRadioTuningQuality() {
  const deviation = Math.abs(50 - state.tuning) / 50;
  const tuningQuality = 1 - deviation;
  audio.setTuning(tuningQuality);

  if (ytPlayer && ytApiReady) {
    const finalVol = Math.max(0, state.volume * tuningQuality);
    ytPlayer.setVolume(finalVol);
  }
}


function playNextTape() {
  const ids = Object.keys(cassetteTracks);
  let idx = ids.indexOf(state.activeCassette);
  if (idx === -1) idx = 0;
  else idx = (idx + 1) % ids.length;
  
  const nextId = ids[idx];
  loadCassette(nextId, cassetteTracks[nextId].ytId);
}

function playPrevTape() {
  const ids = Object.keys(cassetteTracks);
  let idx = ids.indexOf(state.activeCassette);
  if (idx === -1) idx = 0;
  else idx = (idx - 1 + ids.length) % ids.length;
  
  const prevId = ids[idx];
  loadCassette(prevId, cassetteTracks[prevId].ytId);
}

function loadCassette(id, ytId) {
  state.activeCassette = id;
  state.useSynthFallback = false; 

  const track = cassetteTracks[id];
  if (id === 'custom_stream') {
    track.ytId = ytId;
  }

  if (ytPlayer && ytApiReady && typeof ytPlayer.loadVideoById === 'function' && track.ytId) {
    ytPlayer.loadVideoById(track.ytId);
  }

  // Update UI meta details
  document.getElementById('playerSongTitle').textContent = track.title;
  document.getElementById('playerSongArtist').textContent = id === 'custom_stream' ? "YouTube Audio Stream" : "Sleeper Class FM";

  // Update Album Art image
  const albumArt = document.getElementById('playerAlbumArt');
  if (albumArt) {
    if (track.ytId) {
      albumArt.innerHTML = `<img src="https://i.ytimg.com/vi/${track.ytId}/hqdefault.jpg" alt="Art" style="width: 100%; height: 100%; object-fit: cover;">`;
    } else {
      albumArt.textContent = "📀";
    }
  }
  
  // Highlight active dropdown element
  document.querySelectorAll('.glass-playlist-menu .menu-item').forEach(item => {
    item.classList.toggle('active', item.getAttribute('data-id') === id);
  });

  playCassette();
}

function playCassette() {
  if (!state.activeCassette) return;

  if (!audio.initialized) {
    audio.init();
    runVisualFrameTicker();
  }
  audio.resume();

  state.isPlaying = true;
  if (state.useSynthFallback) {
    audio.startSynthTape();
  } else {
    if (ytPlayer && ytApiReady && typeof ytPlayer.playVideo === 'function') {
      audio.stopSynthTape();
      ytPlayer.playVideo();
      setTimeout(() => {
        if (state.isPlaying && !state.useSynthFallback && typeof ytPlayer.getPlayerState === 'function') {
          const s = ytPlayer.getPlayerState();
          if (s !== YT.PlayerState.PLAYING && s !== YT.PlayerState.BUFFERING) {
            console.warn("YouTube playback restricted. Forcing synthesizer fallback...");
            switchToSynthFallback();
          }
        }
      }, 12000);
    } else if (ytPlayer && !ytApiReady) {
      state.playOnReady = true;
      const track = cassetteTracks[state.activeCassette];
      document.getElementById('playerSongTitle').textContent = `Loading Radio... (${track ? track.title : ''})`;
    } else {
      switchToSynthFallback();
    }
  }

  document.getElementById('btnPlayPause').innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor" style="width: 1.1em; height: 1.1em; vertical-align: middle;"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`;
  
  const albumArt = document.getElementById('playerAlbumArt');
  if (albumArt) albumArt.classList.add('album-art-playing');
}

function pauseCassette() {
  if (!state.isPlaying) return;
  state.isPlaying = false;

  if (state.useSynthFallback) {
    audio.stopSynthTape();
  } else {
    if (ytPlayer && ytApiReady && typeof ytPlayer.pauseVideo === 'function') {
      ytPlayer.pauseVideo();
    }
  }

  document.getElementById('btnPlayPause').innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor" style="width: 1.1em; height: 1.1em; vertical-align: middle;"><path d="M8 5v14l11-7z"/></svg>`;
  
  const albumArt = document.getElementById('playerAlbumArt');
  if (albumArt) albumArt.classList.remove('album-art-playing');
}

function stopCassette() {
  state.isPlaying = false;
  
  if (state.useSynthFallback) {
    audio.stopSynthTape();
  } else {
    if (ytPlayer && ytApiReady) {
      ytPlayer.stopVideo();
    }
  }

  document.getElementById('btnPlayPause').innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor" style="width: 1.1em; height: 1.1em; vertical-align: middle;"><path d="M8 5v14l11-7z"/></svg>`;
  
  const albumArt = document.getElementById('playerAlbumArt');
  if (albumArt) albumArt.classList.remove('album-art-playing');
}

// 🚂 Cozy acoustic spatial sound collage for Chai vendor
function callChaiWallahVoice() {
  if (!audio.initialized) audio.init();
  audio.resume();

  const btn = document.getElementById('btnChai');

  // Toggle play/stop if clicked again
  if (state.isChaiPlaying) {
    stopChaiWallahVoice();
    return;
  }

  state.isChaiPlaying = true;
  btn.classList.add('active');

  const now = audio.ctx.currentTime;
  
  // Play PA Mains hum to mimic station PA broadcast
  audio.triggerPAStatic(true, 7500);

  // Play a distant Indian conductor whistle call (rhythmic sound collage)
  const playWhistle = (freq, offset, duration) => {
    const osc = audio.ctx.createOscillator();
    const vibrato = audio.ctx.createOscillator();
    const vibGain = audio.ctx.createGain();
    const gain = audio.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, now + offset);

    vibrato.frequency.setValueAtTime(8, now + offset); // 8Hz vibrato
    vibGain.gain.setValueAtTime(15, now + offset);

    vibrato.connect(vibGain);
    vibGain.connect(osc.frequency);

    gain.gain.setValueAtTime(0, now + offset);
    gain.gain.linearRampToValueAtTime(0.08, now + offset + 0.05);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + offset + duration);

    osc.connect(gain);
    gain.connect(audio.masterGain);

    vibrato.start(now + offset);
    osc.start(now + offset);
    vibrato.stop(now + offset + duration + 0.1);
    osc.stop(now + offset + duration + 0.1);
  };

  // Play clinking of tea glasses
  const playGlassClink = (freq, offset) => {
    const clinkOsc = audio.ctx.createOscillator();
    const clinkGain = audio.ctx.createGain();
    clinkOsc.type = 'sine';
    clinkOsc.frequency.setValueAtTime(freq, now + offset);
    
    clinkGain.gain.setValueAtTime(0, now + offset);
    clinkGain.gain.linearRampToValueAtTime(0.12, now + offset + 0.01);
    clinkGain.gain.exponentialRampToValueAtTime(0.0001, now + offset + 0.4);
    
    clinkOsc.connect(clinkGain);
    clinkGain.connect(audio.masterGain);
    
    clinkOsc.start(now + offset);
    clinkOsc.stop(now + offset + 0.5);
  };

  // Sequence the atmospheric platform collage (Whistle -> Glasses Clinking)
  playWhistle(1600, 0.0, 0.8);  // Station platform whistle blown
  playWhistle(1600, 1.2, 0.4);

  // Vendor footsteps & glasses rattling as they walk past compartment
  window.chaiTimeoutIds = [];
  const scheduleClink = (freq, offset, delay) => {
    const id = setTimeout(() => playGlassClink(freq, offset), delay);
    window.chaiTimeoutIds.push(id);
  };

  scheduleClink(2900, 0.0, 1600);
  scheduleClink(3300, 0.1, 1700);
  scheduleClink(2900, 0.6, 2200);
  scheduleClink(3100, 0.7, 2300);
  scheduleClink(2800, 1.5, 3100);
  scheduleClink(3200, 1.6, 3200);
  scheduleClink(2900, 2.5, 4100);
  scheduleClink(3300, 3.2, 4800);

  // Play the actual WebM chai vendor audio clip!
  if (!window.chaiAudio) {
    window.chaiAudio = new Audio('/chai_chai.webm');
  }
  
  // Set playback volume based on master volume, mute state, and light levels (quieter at night)
  let vendorVol = state.isAmbienceMuted ? 0 : (state.volume / 100) * 0.95;
  if (!state.isLightOn) {
    vendorVol *= 0.45; // Muffled/quieter vendor call during night time
  }
  
  window.chaiAudio.volume = vendorVol;
  window.chaiAudio.currentTime = 0;
  
  window.chaiAudio.addEventListener('ended', () => {
    state.isChaiPlaying = false;
    btn.classList.remove('active');
    audio.triggerPAStatic(false);
  });
  
  window.chaiAudio.play().catch(err => {
    console.warn("Failed to play chai WebM file:", err);
    state.isChaiPlaying = false;
    btn.classList.remove('active');
    audio.triggerPAStatic(false);
  });
}

function stopChaiWallahVoice() {
  state.isChaiPlaying = false;
  const btn = document.getElementById('btnChai');
  if (btn) btn.classList.remove('active');

  if (window.chaiTimeoutIds) {
    window.chaiTimeoutIds.forEach(id => clearTimeout(id));
    window.chaiTimeoutIds = [];
  }

  if (window.chaiAudio) {
    window.chaiAudio.pause();
    window.chaiAudio.currentTime = 0;
  }

  if (audio && typeof audio.triggerPAStatic === 'function') {
    audio.triggerPAStatic(false);
  }
}

// 🔔 Indian Railways authentic PA voice announcer
function playIndianRailwayAnnouncements() {
  if (!audio.initialized) audio.init();
  audio.resume();

  const btn = document.getElementById('btnAnnounce');

  // Toggle play/stop if clicked again
  if (state.isAnnouncementPlaying) {
    stopIndianRailwayAnnouncements();
    return;
  }

  state.isAnnouncementPlaying = true;
  btn.classList.add('active');

  const now = audio.ctx.currentTime;
  
  // Play PA mains hum during the announcement
  audio.triggerPAStatic(true, 12000);

  // Play the iconic 4-note railway chime bell (Ting-Ting-Ting-Ting)
  const playBell = (freq, offset, length) => {
    const osc = audio.ctx.createOscillator();
    const gain = audio.ctx.createGain();
    
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, now + offset);
    
    gain.gain.setValueAtTime(0, now + offset);
    gain.gain.linearRampToValueAtTime(0.12, now + offset + 0.04);
    gain.gain.exponentialRampToValueAtTime(0.001, now + offset + length - 0.04);
    
    osc.connect(gain);
    gain.connect(audio.masterGain);
    
    osc.start(now + offset);
    osc.stop(now + offset + length);
  };

  playBell(392, 0.0, 0.7);  // G4
  playBell(494, 0.35, 0.7); // B4
  playBell(587, 0.7, 0.7);  // D5
  playBell(784, 1.05, 1.2); // G5

  // Trigger the station announcement audio file after the bell chime
  window.announceTimeoutId = setTimeout(() => {
    if (window.announceAudio) {
      window.announceAudio.pause();
    }
    window.announceAudio = new Audio('/station_announce.m4a');

    let announceVol = state.isAmbienceMuted ? 0 : (state.volume / 100) * 0.95;
    if (!state.isLightOn) {
      announceVol *= 0.45; // Quieter/muffled at night
    }

    window.announceAudio.volume = announceVol;
    window.announceAudio.currentTime = 0;
    
    window.announceAudio.addEventListener('ended', () => {
      state.isAnnouncementPlaying = false;
      btn.classList.remove('active');
      audio.triggerPAStatic(false);
    });

    window.announceAudio.play().catch(err => {
      console.warn("Failed to play station announcement audio:", err);
      // Clean up state if it fails to play
      state.isAnnouncementPlaying = false;
      btn.classList.remove('active');
      audio.triggerPAStatic(false);
    });
  }, 2200);
}

function stopIndianRailwayAnnouncements() {
  state.isAnnouncementPlaying = false;
  const btn = document.getElementById('btnAnnounce');
  if (btn) btn.classList.remove('active');
  
  if (window.announceTimeoutId) {
    clearTimeout(window.announceTimeoutId);
    window.announceTimeoutId = null;
  }
  
  if (window.announceAudio) {
    window.announceAudio.pause();
    window.announceAudio.currentTime = 0;
  }
  
  if (audio && typeof audio.triggerPAStatic === 'function') {
    audio.triggerPAStatic(false);
  }
}

function setupKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if (document.activeElement.tagName === 'INPUT') return;

    switch (e.code) {
      case 'Space':
        e.preventDefault();
        if (state.activeCassette) {
          if (state.isPlaying) pauseCassette();
          else playCassette();
        }
        break;
      case 'KeyH':
        document.getElementById('btnHorn').dispatchEvent(new Event('mousedown'));
        break;
      case 'KeyC':
        callChaiWallahVoice();
        break;
      case 'KeyE':
        triggerBrakesSequence();
        break;
    }
  });

  document.addEventListener('keyup', (e) => {
    if (e.code === 'KeyH') {
      document.dispatchEvent(new Event('mouseup'));
    }
  });
}

const trainTypes = {
  rajdhani: { speed: 4.0, angle: 0, name: "Rajdhani Exp" },
  passenger: { speed: 1.35, angle: 90, name: "Local Passenger" },
  steam: { speed: 2.0, angle: 180, name: "Steam Heritage" },
  goods: { speed: 0.65, angle: 270, name: "Freight Train" }
};

function setTrainType(type) {
  state.trainType = type;
  audio.playSwitchClick();

  const config = trainTypes[type];
  
  // Rotate the dial notch
  const dial = document.getElementById('trainDial');
  if (dial) {
    dial.style.transform = `rotate(${config.angle}deg)`;
  }

  // Update active label styling
  document.querySelectorAll('.train-label').forEach(lbl => {
    lbl.classList.toggle('active', lbl.getAttribute('data-type') === type);
  });

  // Dynamically update audio engine target speed
  audio.targetTrainSpeedVal = config.speed;

  // Update Spotify player sub-artist label to display active engine type
  const artistEl = document.getElementById('playerSongArtist');
  if (state.activeCassette) {
    artistEl.textContent = `Sleeper Class FM // ${config.name}`;
  }
  console.log(`Switched to Train Type: ${config.name} (Speed: ${config.speed}, Dial: ${config.angle}deg)`);
}

function startSkyClock() {
  const clockEl = document.getElementById('skyClock');
  if (!clockEl) return;
  
  const updateTime = () => {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12;
    clockEl.textContent = `${hours}:${minutes} ${ampm}`;
  };
  
  updateTime();
  setInterval(updateTime, 1000);
}
function startSkyOnlineCounter() {
  const counterEl = document.getElementById('onlineCountNumber');
  if (!counterEl) return;
  
  // Create a unique identifier for this tab session
  let tabId = sessionStorage.getItem('sleeper_tab_id');
  if (!tabId) {
    tabId = 'tab_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    sessionStorage.setItem('sleeper_tab_id', tabId);
  }
  
  const heartbeatKey = `sleeper_hb_${tabId}`;
  
  const updateOnlineCount = () => {
    const now = Date.now();
    // Write current heartbeat timestamp
    localStorage.setItem(heartbeatKey, now.toString());
    
    // Manage the shared base passenger count simulation
    let sharedBase = localStorage.getItem('sleeper_shared_base_count');
    let lastUpdate = localStorage.getItem('sleeper_shared_base_last_update');
    
    let baseCount = 20; // default fallback
    
    if (!sharedBase || !lastUpdate) {
      baseCount = Math.floor(18 + Math.random() * 8); // random between 18 and 25
      localStorage.setItem('sleeper_shared_base_count', baseCount.toString());
      localStorage.setItem('sleeper_shared_base_last_update', now.toString());
    } else {
      baseCount = parseInt(sharedBase, 10);
      const lastUpdateTime = parseInt(lastUpdate, 10);
      // Fluctuate every 5 seconds
      if (now - lastUpdateTime > 5000) {
        const change = Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
        baseCount = Math.max(12, Math.min(35, baseCount + change)); // clamp base between 12 and 35
        localStorage.setItem('sleeper_shared_base_count', baseCount.toString());
        localStorage.setItem('sleeper_shared_base_last_update', now.toString());
      }
    }
    let activeTabsCount = 0;
    const keysToRemove = [];
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('sleeper_hb_')) {
        const valStr = localStorage.getItem(key);
        const timestamp = parseInt(valStr, 10);
        
        if (!isNaN(timestamp)) {
          if (now - timestamp < 4000) {
            activeTabsCount++;
          } else {
            keysToRemove.push(key);
          }
        }
      }
    }
    
    // Clean up expired keys
    keysToRemove.forEach(key => localStorage.removeItem(key));
    
    // Total count = base simulated passengers + extra open tabs (clamped to at least 10)
    const finalCount = Math.max(10, baseCount + (activeTabsCount - 1));
    counterEl.textContent = finalCount;
  };
  
  // Clean up heartbeat immediately on close
  window.addEventListener('beforeunload', () => {
    localStorage.removeItem(heartbeatKey);
  });
  
  // Run immediately and then every 1.5 seconds
  updateOnlineCount();
  setInterval(updateOnlineCount, 1500);
}

// ─── Theme Explorer Widget ────────────────────────────────────────────────────
(function() {
  const themeExplorer = document.getElementById('themeExplorer');
  const trigger = document.getElementById('themeExplorerTrigger');
  const closeBtn = document.getElementById('themeExplorerClose');
  if (!themeExplorer || !trigger) return;
  trigger.addEventListener('click', (e) => {
    e.stopPropagation();
    themeExplorer.classList.toggle('open');
  });
  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      themeExplorer.classList.remove('open');
    });
  }
  document.addEventListener('click', (e) => {
    if (!e.target.closest('#themeExplorer')) {
      themeExplorer.classList.remove('open');
    }
  });
})();
