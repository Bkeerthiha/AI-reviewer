// Global voice variable
let synth = window.speechSynthesis;

async function runAudit() {
    const codeInput = document.getElementById('code-input');
    const languageSelect = document.getElementById('language');
    const resContainer = document.getElementById('results-container');

    const code = codeInput.value.trim();
    const language = languageSelect.value;

    if (!code) {
        resContainer.innerHTML = `<div class="glass p-8 rounded-[40px] text-red-400 font-bold text-center"> ⚠️ INJECT PAYLOAD! </div>`;
        return;
    }

    resContainer.innerHTML = `<div class="glass p-12 rounded-[50px] text-center animate-pulse italic text-sky-400"> Analyzing... </div>`;

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, language })
        });
        const data = await response.json();

        // Build HTML
        let html = `
            <div class="reveal-card glass p-10 rounded-[45px] border-t-[10px] shadow-2xl" 
                 style="border-color: ${data.color}; opacity: 0; transform: translateY(30px); transition: all 0.8s ease;">
                <p class="text-[10px] font-bold text-slate-500 uppercase mb-2">Audit Score</p>
                <h2 class="text-8xl font-black italic" style="color: ${data.color}">
                    <span id="score-counter">0</span>%
                </h2>
                <p class="text-xs font-black uppercase mt-4 tracking-widest" style="color: ${data.color}">${data.label}</p>
            </div>`;

        data.issues.forEach((issue, idx) => {
            html += `
                <div class="reveal-card glass p-8 rounded-[35px] border-l-[12px] mt-4 shadow-xl" 
                     style="border-color: ${issue.color}; opacity: 0; transform: translateY(20px); transition: all 0.6s ease; transition-delay: ${(idx + 1) * 150}ms">
                    <p class="text-lg font-bold text-white mb-2">${issue.msg}</p>
                    <div class="bg-black/30 p-4 rounded-xl text-[11px] text-slate-400 border border-white/5">
                        <b>AI FIX:</b> ${issue.explain}
                    </div>
                </div>`;
        });

        resContainer.innerHTML = html;

        // Trigger Animations & Voice
        setTimeout(() => {
            const cards = document.querySelectorAll('.reveal-card');
            cards.forEach(c => { c.style.opacity = "1"; c.style.transform = "translateY(0)"; });
            
            animateScore(0, data.score);
            speakFeedback(data.score, data.label);
        }, 100);

    } catch (err) {
        resContainer.innerHTML = `<div class="glass p-8 rounded-[40px] text-red-500 font-black"> ❌ OFFLINE </div>`;
    }
}

// 🔢 Score Counter
function animateScore(start, end) {
    let current = start;
    const counter = document.getElementById('score-counter');
    const duration = 1000;
    const startTime = performance.now();

    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        current = Math.floor(progress * end);
        counter.innerText = current;
        if (progress < 1) requestAnimationFrame(update);
        else counter.innerText = end;
    }
    requestAnimationFrame(update);
}

// 🎤 Guaranteed Voice Logic
function speakFeedback(score, label) {
    // Stop any current speech
    synth.cancel();

    const text = `Scan complete. Your score is ${score} percent. Status is ${label}.`;
    const utterThis = new SpeechSynthesisUtterance(text);
    
    // Voice selection with fallback
    const voices = synth.getVoices();
    utterThis.voice = voices.find(v => v.lang.includes('en-US')) || voices[0];
    
    utterThis.pitch = 1;
    utterThis.rate = 0.9;
    utterThis.volume = 1;

    // Error handling for voice
    utterThis.onerror = (e) => console.error("Speech error:", e);

    synth.speak(utterThis);
}