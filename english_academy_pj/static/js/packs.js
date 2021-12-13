const taskForm = document.getElementById("task-form");

const newBtn = document.getElementById("add-task");

const packsDatabox = document.getElementById("packs-data-box");
const packInput = document.getElementById("packs");

const packText = document.getElementById("pack-text");

const lessonsDatabox = document.getElementById("lessons-data-box");
const lessonInput = document.getElementById("lessons");

const lessonText = document.getElementById("lesson-text");

const teachersDatabox = document.getElementById("teachers-data-box");
const teacherInput = document.getElementById("teachers");

const teacherText = document.getElementById("teacher-text");

const btnBox = document.getElementById("btn-box");
const alertBox = document.getElementById("alert-box");

const dateBox = document.getElementById("date-box");
const dateInput = document.getElementById("date");

const csrf = document.getElementsByName("csrfmiddlewaretoken");

const user_idText = JSON.parse(document.getElementById("user_id").textContent);

let selectedLanguage = "";

newBtn.addEventListener("click", (e) => {
  packsDatabox.innerHTML = "";
  packText.textContent = "Choose a pack";
  packText.classList.add("default");

  dateInput.value = "";
  dateInput.setAttribute("placeholder", "Choose a date");

  $.ajax({
    type: "GET",
    url: "/packs-json/",
    success: function (response) {
      console.log(response.data);
      const packsData = response.data;
      packsData.map((item) => {
        const option = document.createElement("div");
        option.textContent = item.name;
        option.setAttribute("class", "item");
        option.setAttribute("data-value", item.name);
        packsDatabox.appendChild(option);
        selectedLanguage = item.language;
      });
    },
    error: function (error) {
      console.log(error);
    },
  });
});

packInput.addEventListener("change", (e) => {
  const selectedPack = e.target.value;

  lessonsDatabox.innerHTML = "";
  lessonText.textContent = "Choose a lesson";
  lessonText.classList.add("default");

  teachersDatabox.innerHTML = "";
  teacherText.textContent = "Choose a teacher";
  teacherText.classList.add("default");
  btnBox.classList.add("invisible");

  $.ajax({
    type: "GET",
    url: `/lessons-json/${selectedPack}/`,
    success: function (response) {
      console.log(response.data);
      const lessonsData = response.data;
      lessonsData.map((item) => {
        const option = document.createElement("div");
        option.textContent = item.title;
        option.setAttribute("class", "item");
        option.setAttribute("data-value", item.title);
        lessonsDatabox.appendChild(option);
      });
    },
    error: function (error) {
      console.log(error);
    },
  });
});

lessonInput.addEventListener("change", (e) => {
  teachersDatabox.innerHTML = "";
  teacherText.textContent = "Choose a teacher";
  teacherText.classList.add("default");
  $.ajax({
    type: "GET",
    url: `/teachers-json/${selectedLanguage}/`,
    success: function (response) {
      const teachersData = response.data;
      console.log(teachersData);
      teachersData.map((item) => {
        const option = document.createElement("div");
        option.textContent = item.name;
        option.setAttribute("class", "item");
        option.setAttribute("data-value", item.name);
        teachersDatabox.appendChild(option);
      });
      teacherInput.addEventListener("change", (e) => {
        btnBox.classList.remove("invisible");
      });
    },
    error: function (error) {
      console.log(error);
    },
  });
});

dateInput.addEventListener("keydown", (e) => {
  e.preventDefault();
  e.stopImmediatePropagation();
});

dateInput.addEventListener("contextmenu", (e) => {
  e.preventDefault();
  e.stopImmediatePropagation();
});

taskForm.addEventListener("submit", (e) => {
  e.preventDefault();
  //   console.log("submited");
  //   console.log(languageInput.value);
  //   console.log(user_id);

  $.ajax({
    type: "POST",
    url: "/create-task/",
    data: {
      csrfmiddlewaretoken: csrf[0].value,
      pack: packText.textContent,
      lesson: lessonText.textContent,
      date: dateInput.value,
      language: selectedLanguage,
      user_id: user_idText,
    },
    success: function (response) {
      // Task already exists, lesson, teacher and date are busy, please try again
      //   console.log(response);
      if (response.message) {
        alertBox.innerHTML = `<div class="ui negative message">    
                                <i class="close icon"></i>
                                <div class="header">
                                    Ops.
                                </div>
                                <p>Task already exists, lesson, teacher and date are busy, please try again</p>
                            </div>`;
      } else {
        alertBox.innerHTML = `<div class="ui success message">    
                                <i class="close icon"></i>
                                <div class="header">
                                    Success.
                                </div>
                                <p>Your task has been created</p>
                            </div>`;
      }
      $(function () {
        $("#add-task-modal").modal("toggle");
      });
      setTimeout(() => {
        alertBox.innerHTML = "";
      }, 3000);
    },
    error: function (error) {
      alertBox.innerHTML = `<div class="ui negative message">    
                                <i class="close icon"></i>
                                <div class="header">
                                    Ops.
                                </div>
                                <p>Something went wrong</p>
                            </div>`;
      $(function () {
        $("#add-task-modal").modal("toggle");
      });
      setTimeout(() => {
        alertBox.innerHTML = "";
      }, 3000);
    },
  });
});
