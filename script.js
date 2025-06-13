setInterval(() => {
  const now = new Date();
  const timeElement = document.getElementById('time');
  const dateElement = document.getElementById('date');
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const day = now.getDay();
  const months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
  const daysOfWeek = ['일', '월', '화', '수', '목', '금', '토'];

  timeElement.textContent = `${hours}:${minutes < 10 ? '0' + minutes : minutes}`;
  dateElement.textContent = `${daysOfWeek[day]}, ${months[now.getMonth()]} ${now.getDate()}`;
}, 1000);

function openMessage() {
  window.location.href = 'imessage.html';
}
