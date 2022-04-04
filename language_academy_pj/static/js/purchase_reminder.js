const userPercentText = JSON.parse(
  document.getElementById("user_booking_percent").textContent
);

setTimeout(() => {
  let today = new Date().toLocaleDateString();

  if (localStorage.getItem("reminder") === null) {
    if (userPercentText >= 90) {
      localStorage.setItem("reminder", today);
      $("#purchase-reminder-modal").modal("show");
    }
  }

  if (localStorage.getItem("reminder") !== today) {
    if (userPercentText >= 90) {
      $("#purchase-reminder-modal").modal("show");
    }
  }
}, 5000);
