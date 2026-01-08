
import streamlit as st

st.set_page_config(layout="wide")
st.title("🎹 フル機能ピアノ (黒鍵・録音・再生・キーボード演奏)")

# ====== ピアノ鍵盤構成（2オクターブ） ======
keys = [
    ("C4", 261.63), ("C#4", 277.18), ("D4", 293.66), ("D#4", 311.13), ("E4", 329.63),
    ("F4", 349.23), ("F#4", 369.99), ("G4", 392.00), ("G#4", 415.30), ("A4", 440.00), ("A#4", 466.16), ("B4", 493.88),
    ("C5", 523.25), ("C#5", 554.37), ("D5", 587.33), ("D#5", 622.25), ("E5", 659.25),
    ("F5", 698.46), ("F#5", 739.99), ("G5", 783.99), ("G#5", 830.61), ("A5", 880.00), ("A#5", 932.33), ("B5", 987.77)
]

# ===== HTML + CSS + JS ======
html = """
<style>
.piano-wrap { display:flex; position:relative; height:260px; }
.white-key {
    width:50px; height:260px; border:1px solid #333;
    background:white; z-index:1; position:relative;
    display:flex; justify-content:center; align-items:flex-end;
    padding-bottom:10px;
    font-size:14px; cursor:pointer; user-select:none;
    transition: background 0.1s;
}
.white-key.active { background:#aaf; }

.black-key {
    width:35px; height:160px; background:black;
    position:absolute; margin-left:-18px; z-index:2;
    border-radius:0 0 4px 4px;
    cursor:pointer; user-select:none;
    color:white; display:flex; justify-content:center;
    align-items:flex-end; padding-bottom:5px;
    font-size:12px;
    transition: background 0.1s;
}
.black-key.active { background:#55f; }
</style>

<div class="piano-wrap">
"""

# 白鍵と黒鍵を配置
white_positions = []
white_idx = 0
for i, (name, freq) in enumerate(keys):
    is_black = "#" in name
    if not is_black:
        html += f'<div class="white-key" data-name="{name}" data-freq="{freq}" id="key-{name}">{name}</div>'
        white_positions.append(name)
    else:
        # 黒鍵の位置を白鍵の上に重ねて配置
        html += f'''
        <div class="black-key" data-name="{name}" data-freq="{freq}"
             style="left:{white_idx*50 + 35}px" id="key-{name}">
            {name}
        </div>
        '''
    if not is_black:
        white_idx += 1

html += "</div>"

# JavaScript: 音生成、アニメーション、録音・再生
js = """
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

// 録音用
let recording = [];
let isRecording = false;

// キー対応
const keyMap = {
    'a': 'C4', 'w': 'C#4', 's': 'D4', 'e': 'D#4', 'd': 'E4',
    'f': 'F4', 't': 'F#4', 'g': 'G4', 'y': 'G#4', 'h': 'A4',
    'u': 'A#4', 'j': 'B4',
    'k': 'C5', 'o': 'C#5', 'l': 'D5', 'p': 'D#5', ';': 'E5'
};

function playNote(name, freq){
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = "sine";
    osc.frequency.value = freq;
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    gain.gain.setValueAtTime(1, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);

    osc.start();
    osc.stop(audioCtx.currentTime + 0.5);

    const el = document.getElementById(`key-${name}`);
    el.classList.add("active");
    setTimeout(() => el.classList.remove("active"), 200);

    if(isRecording){
        recording.push({name:name, freq:freq, time:Date.now()});
    }
}

document.querySelectorAll('.white-key, .black-key').forEach((key)=>{
    key.addEventListener('click', ()=>{
        playNote(key.dataset.name, key.dataset.freq);
    });
});

document.addEventListener('keydown', (e)=>{
    const key = e.key;
    if(keyMap[key]){
        const targetName = keyMap[key];
        const el = document.querySelector(`[data-name="${targetName}"]`);
        if(el){
            playNote(targetName, el.dataset.freq);
        }
    }
});

// Start / Stop Recording
window.startRecording = () => {
    recording = [];
    isRecording = true;
};

window.stopRecording = () => {
    isRecording = false;
    return recording;
};

// Replay recording
window.playRecording = (rec) => {
    if(!rec || rec.length === 0) return;
    const start = rec[0].time;
    rec.forEach(note => {
        setTimeout(()=>{
            playNote(note.name, note.freq);
        }, note.time - start);
    });
};
"""

st.markdown(html, unsafe_allow_html=True)
st.html(f"<script>{js}</script>")

# 録音操作用ボタン
st.write("## 🎼 録音コントロール")
col1, col2, col3 = st.columns(3)

if col1.button("🎙 録音開始"):
    st.session_state["record"] = "start"

if col2.button("⏹ 録音停止"):
    st.session_state["record"] = "stop"

if col3.button("▶ 再生"):
    st.session_state["record"] = "play"

# JS との連携
st.write("""
<script>
if(window.parent.document){
    const frame = window.parent.document;
}
</script>
""")

if "record" in st.session_state:
    if st.session_state["record"] == "start":
        st.write("<script>startRecording();</script>", unsafe_allow_html=True)
    elif st.session_state["record"] == "stop":
        st.write("""
        <script>
        const result = stopRecording();
        window.recordData = result;
        </script>
        """, unsafe_allow_html=True)
    elif st.session_state["record"] == "play":
        st.write("""
        <script>
        if(window.recordData){
            playRecording(window.recordData);
        }
        </script>
        """, unsafe_allow_html=True)
