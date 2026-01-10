import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Streamlit Recording Piano", layout="centered")

st.title("🎹 Recording Piano")
st.write("「Record」を押して演奏し、「Stop」のあとに「Play」で再生できます。")

piano_html = """
<style>
    .controls { text-align: center; margin-bottom: 20px; }
    .btn { padding: 10px 20px; margin: 5px; cursor: pointer; font-weight: bold; border-radius: 5px; border: none; }
    .record { background: #ff4b4b; color: white; }
    .stop { background: #555; color: white; }
    .play { background: #28a745; color: white; }
    
    .piano { display: flex; justify-content: center; }
    .key {
        width: 50px; height: 180px; border: 1px solid #333; background: white;
        cursor: pointer; display: flex; flex-direction: column; align-items: center; 
        justify-content: flex-end; padding-bottom: 15px; font-weight: bold;
        font-size: 12px; line-height: 1.2; text-align: center; user-select: none; 
        margin: 0 2px; border-radius: 0 0 5px 5px;
    }
    .black-key {
        width: 35px; height: 110px; background: #222; color: white;
        margin-left: -20px; margin-right: -20px; z-index: 2; border-radius: 0 0 3px 3px;
    }
    .key.active { background: #ffcc00 !important; }
</style>

<div class="controls">
    <button class="btn record" onclick="startRecording()">🔴 Record</button>
    <button class="btn stop" onclick="stopRecording()">⏹️ Stop</button>
    <button class="btn play" onclick="playRecording()">▶️ Play</button>
</div>

<div class="piano">
    <div id="key-A" class="key" onclick="playNote(261.63, 'key-A')">ド<br>A</div>
    <div id="key-W" class="key black-key" onclick="playNote(277.18, 'key-W')">ド#<br>W</div>
    <div id="key-S" class="key" onclick="playNote(293.66, 'key-S')">レ<br>S</div>
    <div id="key-E" class="key black-key" onclick="playNote(311.13, 'key-E')">レ#<br>E</div>
    <div id="key-D" class="key" onclick="playNote(329.63, 'key-D')">ミ<br>D</div>
    <div id="key-F" class="key" onclick="playNote(349.23, 'key-F')">ファ<br>F</div>
    <div id="key-T" class="key black-key" onclick="playNote(369.99, 'key-T')">ファ#<br>T</div>
    <div id="key-G" class="key" onclick="playNote(392.00, 'key-G')">ソ<br>G</div>
    <div id="key-Y" class="key black-key" onclick="playNote(415.30, 'key-Y')">ソ#<br>Y</div>
    <div id="key-H" class="key" onclick="playNote(440.00, 'key-H')">ラ<br>H</div>
    <div id="key-U" class="key black-key" onclick="playNote(466.16, 'key-U')">ラ#<br>U</div>
    <div id="key-J" class="key" onclick="playNote(493.88, 'key-J')">シ<br>J</div>
    <div id="key-K" class="key" onclick="playNote(523.25, 'key-K')">ド<br>K</div>
</div>

<script>
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    let recordedNotes = [];
    let isRecording = false;
    let startTime = 0;

    const keyMap = {
        'a': { freq: 261.63, id: 'key-A' }, 'w': { freq: 277.18, id: 'key-W' },
        's': { freq: 293.66, id: 'key-S' }, 'e': { freq: 311.13, id: 'key-E' },
        'd': { freq: 329.63, id: 'key-D' }, 'f': { freq: 349.23, id: 'key-F' },
        't': { freq: 369.99, id: 'key-T' }, 'g': { freq: 392.00, id: 'key-G' },
        'y': { freq: 415.30, id: 'key-Y' }, 'h': { freq: 440.00, id: 'key-H' },
        'u': { freq: 466.16, id: 'key-U' }, 'j': { freq: 493.88, id: 'key-J' },
        'k': { freq: 523.25, id: 'key-K' }
    };

    function playNote(frequency, elementId, save = true) {
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        oscillator.type = 'triangle';
        oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);
        gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.8);
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        oscillator.start();
        oscillator.stop(audioCtx.currentTime + 0.8);

        const el = document.getElementById(elementId);
        if(el) {
            el.classList.add('active');
            setTimeout(() => el.classList.remove('active'), 150);
        }

        // 録音中の場合、タイミングと周波数を保存
        if (isRecording && save) {
            recordedNotes.push({
                freq: frequency,
                id: elementId,
                time: Date.now() - startTime
            });
        }
    }

    function startRecording() {
        recordedNotes = [];
        isRecording = true;
        startTime = Date.now();
        console.log("Recording started...");
    }

    function stopRecording() {
        isRecording = false;
        console.log("Recording stopped. Total notes:", recordedNotes.length);
    }

    function playRecording() {
        if (recordedNotes.length === 0) return;
        recordedNotes.forEach(note => {
            setTimeout(() => {
                playNote(note.freq, note.id, false);
            }, note.time);
        });
    }

    window.addEventListener('keydown', (e) => {
        const keyData = keyMap[e.key.toLowerCase()];
        if (keyData && !e.repeat) {
            playNote(keyData.freq, keyData.id);
        }
    });
</script>
"""

components.html(piano_html, height=450)
st.success("キーボードの「A-S-D-F」の列を使って、左手で伴奏、右手でメロディを弾く練習もできます。")