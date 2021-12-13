const taskForm = document.getElementById("form-event");
const deleteForm = document.getElementById("delete-form");

const newBtn = document.getElementById("add-task");

const teacherSelect = document.getElementById("new-teacher");

const dateInput = document.getElementById("new-date");
const timeInput = document.getElementById("ctimepicker");

const csrf = document.getElementsByName("csrfmiddlewaretoken");

const alertBox = document.getElementById("alert-box");
const alertDeleteBox = document.getElementById("alert-delete-box");
const spinnerBox = document.getElementById("spinner-box");
const spinnerDeleteBox = document.getElementById("spinner-delete-box");

const user_idText = JSON.parse(document.getElementById("user_id").textContent);

const taskModalTitle = document.getElementById("task-modal-title");

const lessonContainer = document.getElementById("lesson-container");

const lessonLink = document.getElementById("lesson-link");

const lesson = document.getElementById("new-lesson");

const taskCount = document.getElementById("task-hours");

const updateUrl = window.location.href + "update/";
const deleteUrl = window.location.href + "delete/";

let selectedLanguage = "";
let taskId = "";
let taskStatus = "";
let totalLessonHours = 0;
let taskHours = parseInt(taskCount.textContent);

let currentTeacher = "";
let teacherId = "";

var table;

function disableDatetimeInput(state) {
  if (state) {
    dateInput.setAttribute("disabled", true);
    timeInput.setAttribute("disabled", true);
  } else {
    dateInput.removeAttribute("disabled");
    timeInput.removeAttribute("disabled");
  }
}

function disabledWeekDays(enabledDays) {
  let week_days = enabledDays.toString().split(",").map(Number);
  let days = [0, 1, 2, 3, 4, 5, 6];
  let disabled_week_days = days.filter((day) => !week_days.includes(day));

  $(".datepicker").datepicker("setDaysOfWeekDisabled", disabled_week_days);
}

function hoursDisabled(enabledHours) {
  let hours = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23,
  ];
  let h = enabledHours.toString().split(",").map(Number);
  let disabled_hours = hours.filter((hour) => !h.includes(hour));
  //   let hoursToString = disabled_hours.toString().split(",");
  let dH = [];
  let maxTm = null;
  let convert24To12 = disabled_hours.forEach((hour) => {
    let m = hour >= 12 ? "pm" : "am";
    let temp = "";

    hour %= 12;
    hour = hour ? hour : 12;
    maxTm = hour === 11 ? (m === "pm" ? "10pm" : null) : null;
    temp =
      hour +
      m +
      ", " +
      (hour === 12 ? "1" : hour + 1) +
      (hour === 11 ? (m === "am" ? "pm" : "am") : m);
    dH.push(temp.toString().split(","));
  });

  $("#ctimepicker").timepicker({
    step: 60,
    timeFormat: "h:i A",
    scrollDefault: "now",
    disableTimeRanges: dH,
    maxTime: maxTm,
  });
}

teacherSelect.addEventListener("change", (e) => {
  $(".datepicker").datepicker("clearDates", true);
  timeInput.value = "";
  let hours = e.target.selectedOptions[0].dataset.hours;
  hoursDisabled(hours);
  let week_days = e.target.selectedOptions[0].dataset.week_days;
  //     .split(",")
  //     .map(Number);

  //   let days = [0, 1, 2, 3, 4, 5, 6];
  //   let disabled_week_days = days.filter((day) => !week_days.includes(day));

  //   $(".datepicker").datepicker("setDaysOfWeekDisabled", disabled_week_days);
  disabledWeekDays(week_days);

  disableDatetimeInput(false);
});

$(document).ready(function () {
  ("use strict");
  table = $("#tasks-datatable").DataTable({
    language: {
      paginate: {
        previous: "<i class='mdi mdi-chevron-left'>",
        next: "<i class='mdi mdi-chevron-right'>",
      },
      info: "Showing bookings _START_ to _END_ of _TOTAL_",
      lengthMenu:
        'Display <select class=\'form-select form-select-sm ms-1 me-1\'><option value="10">10</option><option value="20">20</option><option value="-1">All</option></select> tasks',
    },
    pageLength: 10,
    columns: [
      {
        orderable: !1,
      },
      { orderable: !1 },
      { orderable: !1 },
      { orderable: !1 },
      {
        orderable: !1, //orderSequence: ["desc"],
      },
      { orderable: !1 },
      { orderable: !1 },
    ],
    order: false,
    select: { style: "multi" },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded"),
        $("#tasks-datatable_length label").addClass("form-label");
    },
  });
});

function open_edit_modal(id, lessonNumber, teacherName, teacherUserId) {
  taskId = id;
  taskModalTitle.textContent = "Edit booking";
  teacherSelect.innerHTML = "";
  timeInput.value = "";
  $(".datepicker").datepicker("clearDates", true);

  lesson.value = "";
  currentTeacher = teacherName;
  teacherId = teacherUserId;

  $.ajax({
    type: "GET",
    url: `/get-task/${id}/`,
    success: function (response) {
      const taskData = response.data;
      taskData.map((item) => {
        lesson.value = lessonNumber;
        selectedLanguage = item.language;
        taskStatus = item.status;
        $.ajax({
          type: "GET",
          url: `/teachers-json/${item.language}/`,
          success: function (response) {
            const teachersData = response.data;
            teachersData.map((itemT) => {
              const optionTeacher = document.createElement("OPTION");
              optionTeacher.text = itemT.name;
              optionTeacher.value = itemT.name;
              optionTeacher.setAttribute("data-week_days", itemT.week_days);
              optionTeacher.setAttribute("data-hours", itemT.hours);
              if (itemT.name === currentTeacher) {
                optionTeacher.setAttribute("selected", true);
                disabledWeekDays(itemT.week_days);
                hoursDisabled(itemT.hours);

                let [pDate, pTime] = item.date.split(" ");
                let pHour = pTime.split(":")[0];
                let m = pHour >= 12 ? "PM" : "AM";
                pHour %= 12;
                pHour = (pHour ? pHour : 12) + ":00 ";

                let pDate1 = pDate.split("/");
                dateInput.value =
                  pDate1[0] + "/" + pDate1[1] + "/" + "20" + pDate1[2];
                timeInput.value = pHour + m;
              }
              teacherSelect.appendChild(optionTeacher);
            });
          },
          error: function (error) {
            console.log(error);
          },
        });
      });
      $("#new-task-modal").modal("show");
    },
    error: function (error) {
      console.log(error);
    },
  });
}

function show_lesson_link(link) {
  lessonLink.setAttribute("href", link);
  lessonLink.innerHTML = `<span>${link}</span>`;

  $("#lesson-link-modal").modal("show");
}

function delete_modal(id, status) {
  taskId = id;
  taskStatus = status;
  $("#delete-task-modal").modal("show");
}

const convertTime12to24 = (time12h) => {
  const [time, modifier] = time12h.split(" ");

  let [hours, minutes] = time.split(":");

  if (hours === "12") {
    hours = "00";
  }

  if (modifier === "PM") {
    hours = parseInt(hours, 10) + 12;
  }

  return `${hours}:${minutes}:00.0`;
};

newBtn.addEventListener("click", (e) => {
  taskModalTitle.textContent = "New booking";
  //   taskForm.reset();
  teacherSelect.innerHTML = `<option value="" selected disabled hidden>Select a teacher</option>`;
  $(".datepicker").datepicker("clearDates", true);
  timeInput.value = "";
  disableDatetimeInput(true);
  lesson.value = "";
  totalLessonHours = 0;

  //adding new hour
  $.ajax({
    type: "GET",
    url: "/packs-json/",
    success: function (response) {
      const packsData = response.data;
      packsData.map((item) => {
        selectedLanguage = item.language;
        totalLessonHours += item.number_of_lessons;
      });
      if (totalLessonHours - taskHours > 0) {
        lesson.value = taskHours + 1;
        $.ajax({
          type: "GET",
          url: `/teachers-json/${selectedLanguage}/`,
          success: function (response) {
            const teachersData = response.data;
            teachersData.map((item) => {
              const option = document.createElement("OPTION");
              option.text = item.name;
              option.value = item.name;
              option.setAttribute("data-user_id", item.user_id);
              option.setAttribute("data-week_days", item.week_days);
              option.setAttribute("data-hours", item.hours);
              teacherSelect.appendChild(option);
            });
          },
          error: function (error) {
            console.log(error);
          },
        });
      } else {
        lesson.value = "You have no more class hours, go to support and sales";
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
});

taskForm.addEventListener("submit", (e) => {
  e.preventDefault();

  spinnerBox.innerHTML = '<div class="spinner-border" role="status"></div>';

  if (taskModalTitle.textContent === "New booking") {
    if (totalLessonHours - taskHours <= 0) {
      $("#new-task-modal").modal("toggle");
      spinnerBox.innerHTML = "";
    } else {
      if (
        timeInput.value.length === 0 ||
        dateInput.value.length === 0 ||
        teacherSelect.value.length === 0
      ) {
        spinnerBox.innerHTML = "";
      } else {
        let dateStr = dateInput.value.split("/").reverse().join("-");
        let timeStr = convertTime12to24(timeInput.value);
        teacherId =
          teacherSelect[teacherSelect.options.selectedIndex].getAttribute(
            "data-user_id"
          );
        $.ajax({
          type: "POST",
          url: "/create-task/",
          data: {
            csrfmiddlewaretoken: csrf[0].value,
            // pack: packSelect.value,
            lesson: lesson.value,
            teacher: teacherSelect.value,
            teacher_user_id: teacherId,
            date: dateStr + " " + timeStr,
            language: selectedLanguage,
            user_id: user_idText,
          },
          success: function (response) {
            spinnerBox.innerHTML = "";
            // Task already exists, lesson, teacher and date are busy, please try again
            if (response.message) {
              alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                      <i class="dripicons-wrong me-2"></i> <strong>Ups</strong>. Booking already exists. Teacher and date are busy.
                      </div>`;
              setTimeout(() => {
                $("#new-task-modal").modal("toggle");
                alertBox.innerHTML = "";
              }, 2000);
            } else {
              alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                        <i class="dripicons-checkmark me-2"></i><strong>success</strong>. Your booking has been created
                                                </div>`;
              setTimeout(() => {
                $("#new-task-modal").modal("toggle");
                alertBox.innerHTML = "";
                window.location.reload();
              }, 2000);
            }
          },
          error: function (error) {
            spinnerBox.innerHTML = "";
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                            <i class="dripicons-wrong me-2"></i> <strong>Ups</strong>. Something went wrong.
                        </div>`;
            setTimeout(() => {
              $("#add-task-modal").modal("toggle");
              alertBox.innerHTML = "";
            }, 2000);
          },
        });
      }
    }
  } else if (taskModalTitle.textContent === "Edit booking") {
    if (
      timeInput.value.length === 0 ||
      dateInput.value.length === 0 ||
      teacherSelect.value.length === 0
    ) {
      spinnerBox.innerHTML = "";
    } else {
      let dateStr = dateInput.value.split("/").reverse().join("-");
      let timeStr = convertTime12to24(timeInput.value);
      const d = new Date();
      let taskTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      $.ajax({
        type: "POST",
        url: `/${taskId}/update/`,
        data: {
          csrfmiddlewaretoken: csrf[0].value,
          teacher: teacherSelect.value,
          teacher_user_id: teacherId,
          date: dateStr + " " + timeStr,
          language: selectedLanguage,
          user_id: user_idText,
          status: taskStatus,
          timezone: taskTimezone,
        },
        success: function (response) {
          spinnerBox.innerHTML = "";
          // Task already exists, lesson, teacher and date are busy, please try again
          if (response.message) {
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                      <i class="dripicons-wrong me-2"></i> <strong>Ups</strong>. Booking already exists. Teacher and date are busy.
                      </div>`;
            setTimeout(() => {
              $("#new-task-modal").modal("hide");
              alertBox.innerHTML = "";
            }, 2000);
          } else if (response.msg) {
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                        <i class="dripicons-wrong me-2"></i> ${response.msg}
                        </div>`;
            console.log(response.msg);
            setTimeout(() => {
              $("#new-task-modal").modal("hide");
              alertBox.innerHTML = "";
              if (response.msg === "Booking expired") {
                window.location.reload();
              }
            }, 2000);
          } else {
            alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                        <i class="dripicons-checkmark me-2"></i><strong>success</strong>. Your booking has been updated
                                                </div>`;
            setTimeout(() => {
              $("#new-task-modal").modal("toggle");
              alertBox.innerHTML = "";
              window.location.reload();
            }, 2000);
          }
        },
        error: function (error) {
          spinnerBox.innerHTML = "";
          alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                            <i class="dripicons-wrong me-2"></i> <strong>Ups</strong>.Something went wrong.
                        </div>`;
          setTimeout(() => {
            $("#add-task-modal").modal("hide");
            alertBox.innerHTML = "";
          }, 2000);
        },
      });
    }
  }
});

deleteForm.addEventListener("submit", (e) => {
  e.preventDefault();
  alertDeleteBox.innerHTML = "";
  spinnerDeleteBox.innerHTML =
    '<div class="spinner-border" role="status"></div>';
  $.ajax({
    type: "POST",
    url: `/${taskId}/delete/`,
    data: {
      csrfmiddlewaretoken: csrf[0].value,
      status: taskStatus,
    },
    success: function (response) {
      spinnerDeleteBox.innerHTML = "";
      if (response.msg) {
        alertDeleteBox.innerHTML = `<div class="alert alert-danger" role="alert">
                  <i class="dripicons-checkmark me-2"></i>${response.msg}
                                          </div>`;
        setTimeout(() => {
          $("#delete-task-modal").modal("hide");
          alertDeleteBox.innerHTML = "";
        }, 2000);
      } else {
        alertDeleteBox.innerHTML = `<div class="alert alert-success" role="alert">
                                    <i class="dripicons-checkmark me-2"></i><strong>success</strong>. Your booking has been deleted
                                                            </div>`;
        setTimeout(() => {
          $("#delete-task-modal").modal("hide");
          alertDeleteBox.innerHTML = "";
          window.location.reload();
        }, 2000);
      }
    },
    error: function (error) {
      spinnerDeleteBox.innerHTML = "";
      alertDeleteBox.innerHTML = `<div class="alert alert-danger" role="alert">
                  <i class="dripicons-wrong me-2"></i> <strong>Ups</strong>. Something went wrong.
              </div>`;
      setTimeout(() => {
        $("#delete-task-modal").modal("hide");
        alertBox.innerHTML = "";
      }, 2000);
    },
  });
});
