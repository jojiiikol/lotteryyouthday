// --- ДАННЫЕ (заглушка, заменить на fetch при интеграции) ---
let data;

// Функция инициализации при загрузке страницы
const initializeApp = async () => {
    const token = sessionStorage.getItem('auth_token');
    if (!token) {
        window.location.href = '/front/login.html';
        return;
    }

    // Загружаем данные при инициализации
    await get_users();

};

const get_users = async () => {
    try {
        const response = await fetch(`${GLOBAL_URL}/lottery/get_users`, {
            method: "GET",
            credentials: "include",
            headers: {
                Authorization: "Bearer " + sessionStorage.getItem("auth_token")
            }
        })
        if (response.status === 200) {
            console.log(await response.json())
        }
        if (response.status === 401) {
            sessionStorage.removeItem('auth_token');
            window.location.href = '/front/login.html';
        }
    } catch (error) {
        console.log(error)

    }
}

const fetchData = async () => {
    try {
        const response = await fetch(`${GLOBAL_URL}/lottery/`, {
            method: "POST",
            credentials: "include",
            headers: {
                Authorization: "Bearer " + sessionStorage.getItem("auth_token")
            }
        })
        if (response.status === 404) {
            alert("Нет пользователей на розыгрыш")
        }
        if (response.status === 200) {
            data = await response.json()
        }
        if (response.status === 401) {
            sessionStorage.removeItem('auth_token');
            window.location.href = '/front/login.html';
        }
    } catch (error) {
        console.log(error)
    }
}

const sendMessage = async (tg_id) => {
    console.log(tg_id)
    try {
        const response = await fetch(`${GLOBAL_URL}/bot/${tg_id}`, {
            method: "POST",
            credentials: "include",
            headers: {
                Authorization: "Bearer " + sessionStorage.getItem("auth_token")
            }
        })
        if (response.status === 200) {
            console.log(await response.json())
        }
        if (response.status === 401) {
            sessionStorage.removeItem('auth_token');
            window.location.href = '/front/login.html';
        }
    } catch (error) {
        console.log(error)
    }
}

const numberRoulette = document.getElementById('numberRoulette');
const startBtn = document.getElementById('startBtn');
const winnerModal = document.getElementById('winnerModal');
const winnerInfo = document.getElementById('winnerInfo');
const closeModal = document.getElementById('closeModal');
const confettiCanvas = document.getElementById('confetti');

let isRolling = false;
let animationFrame;
let rollInterval = 60; // ms
let rollTimeout;
let currentId = null;

function shuffle(arr) {
    return arr.map(v => [Math.random(), v]).sort().map(a => a[1]);
}

async function startRoulette() {
    await fetchData();
    if (isRolling) return;
    isRolling = true;
    let ids = data.users.map(u => u.id);
    let speed = 60; // ms
    let slowdown = 1.05;
    let duration = 2000 + Math.random() * 1000;
    let elapsed = 0;
    let winnerId = data.winner.id;
    let lastId = null;

    function roll() {
        if (!isRolling) return;
        elapsed += speed;
        let pool = shuffle(ids);
        let showId = pool[0];
        // Не повторять подряд
        if (showId === lastId && pool.length > 1) showId = pool[1];
        lastId = showId;
        numberRoulette.textContent = showId;
        numberRoulette.style.color = `hsl(${Math.random() * 360},90%,60%)`;
        if (elapsed < duration) {
            speed = Math.max(30, speed * slowdown);
            rollTimeout = setTimeout(roll, speed);
        } else {
            // Плавно замедляем и останавливаемся на победителе
            finishRoll(winnerId, speed);
        }
    }

    roll();
}

function finishRoll(winnerId, speed) {
    let steps = 10;
    let ids = data.users.map(u => u.id);
    let i = 0;

    function slowRoll() {
        if (i < steps - 1) {
            let pool = shuffle(ids.filter(id => id !== winnerId));
            let showId = pool[0];
            numberRoulette.textContent = showId;
            numberRoulette.style.color = `hsl(${Math.random() * 360},90%,60%)`;
            i++;
            setTimeout(slowRoll, speed + i * 30);
        } else {
            numberRoulette.textContent = winnerId;
            numberRoulette.style.color = '#ff8a00';
            isRolling = false;
            setTimeout(() => {
                showWinnerModal();
                launchConfetti();
            }, 600);
        }
    }

    slowRoll();
}

startBtn.onclick = startRoulette;

// --- МОДАЛКА ---
async function showWinnerModal() {
    await sendMessage(data.winner.tg_id);
    winnerInfo.innerHTML = `
    <div class="winner-number">Номер: <span class="number-highlight">${data.winner.id}</span></div>
    <div class="winner-name"><b>${data.winner.name} ${data.winner.last_name}</b></div>
    <div class="winner-details">Пол: ${data.winner.sex === 'male' ? 'Мужской' : 'Женский'}</div>
  `;
    winnerModal.style.display = 'flex';
}

closeModal.onclick = () => {
    winnerModal.style.display = 'none';
    clearConfetti();
};
window.onclick = (e) => {
    if (e.target === winnerModal) {
        winnerModal.style.display = 'none';
        clearConfetti();
    }
};

// --- КОНФЕТТИ ---
function launchConfetti() {
    const ctx = confettiCanvas.getContext('2d');
    confettiCanvas.width = window.innerWidth;
    confettiCanvas.height = window.innerHeight;
    let confetti = [];
    for (let i = 0; i < 150; i++) {
        confetti.push({
            x: Math.random() * confettiCanvas.width,
            y: Math.random() * -confettiCanvas.height,
            r: 6 + Math.random() * 8,
            d: 4 + Math.random() * 6,
            color: `hsl(${Math.random() * 360},90%,60%)`,
            tilt: Math.random() * 10 - 5,
            tiltAngle: 0,
            tiltAngleIncremental: (Math.random() * 0.07) + 0.05
        });
    }

    function draw() {
        ctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
        confetti.forEach(c => {
            ctx.beginPath();
            ctx.ellipse(c.x, c.y, c.r, c.r / 2, c.tilt, 0, 2 * Math.PI);
            ctx.fillStyle = c.color;
            ctx.fill();
        });
        update();
        confettiAnimation = requestAnimationFrame(draw);
    }

    function update() {
        confetti.forEach(c => {
            c.y += c.d;
            c.tiltAngle += c.tiltAngleIncremental;
            c.tilt = Math.sin(c.tiltAngle) * 15;
            c.x += Math.sin(c.tiltAngle);
            if (c.y > confettiCanvas.height) {
                c.x = Math.random() * confettiCanvas.width;
                c.y = -10;
            }
        });
    }

    draw();
}

let confettiAnimation;

function clearConfetti() {
    if (confettiAnimation) cancelAnimationFrame(confettiAnimation);
    const ctx = confettiCanvas.getContext('2d');
    ctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
}

// --- ИНИЦИАЛИЗАЦИЯ ---
initializeApp();