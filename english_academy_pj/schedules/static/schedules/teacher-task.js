const finishForm = document.getElementById("finish-form");

const linkForm = document.getElementById("link-form");
const linkInput = document.getElementById("new-link");
const invalidLink = document.getElementById("invalid-link");
// console.log(linkInput);
// console.log(invalidLink);

const csrf = document.getElementsByName("csrfmiddlewaretoken");

const alertBox = document.getElementById("alert-box");
const spinnerBox = document.getElementById("spinner-box");

const linkAlertBox = document.getElementById("link-alert-box");
const linkSpinnerBox = document.getElementById("link-spinner-box");

let selectedLanguage = "";
let taskId = "";

// const num = document.querySelectorAll("td");
document.addEventListener("DOMContentLoaded", (e) => {
  const num = document.getElementsByClassName("lesson_number");
  let previous_id = null,
    counter = 0;
  for (let i = 0; i < num.length; i++) {
    let student_id = num[i].getAttribute("data-student_id");
    previous_id = previous_id ? previous_id : student_id;

    if (student_id === previous_id) {
      counter++;
    } else {
      counter = 1;
    }

    previous_id = student_id;
    num[i].textContent = counter + " h";
  }
});

// const user_idText = JSON.parse(document.getElementById("user_id").textContent);

function finish_task(id) {
  taskId = id;
  $("#finish-task-modal").modal("show");
}

function task_link(task_id, status) {
  task_id;
  linkInput.classList.remove("is-invalid");
  linkInput.classList.remove("is-valid");
  linkInput.value = "";
  $("#link-modal").modal("show");

  linkForm.addEventListener("submit", (e) => {
    e.preventDefault();
    e.stopPropagation();

    linkAlertBox.innerHTML = "";
    linkSpinnerBox.innerHTML = "";
    let link = linkInput.value;

    let pattern =
      /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/gm;

    if (pattern.test(link)) {
      linkInput.classList.remove("is-invalid");
      linkInput.classList.add("is-valid");
      linkSpinnerBox.innerHTML =
        '<div class="spinner-border" role="status"></div>';
      console.log(`Valid link: ${link}`);
      console.log(`status: ${status}`);

      $.ajax({
        type: "POST",
        url: `/${task_id}/link/`,
        data: {
          csrfmiddlewaretoken: csrf[0].value,
          link: link,
          status: status,
          //   teacher: teacherSelect.value,
          //   teacher_user_id: teacherId,
          //   date: dateStr + " " + timeStr,
          //   language: selectedLanguage,
          //   user_id: user_idText,
        },
        success: function (response) {
          linkSpinnerBox.innerHTML = "";
          if (response.msg === "expired") {
            linkAlertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                        <i class="dripicons-wrong me-2"></i> <strong>fail.</strong> Booking expired.
                        </div>`;
            setTimeout(() => {
              $("#new-task-modal").modal("hide");
              linkAlertBox.innerHTML = "";
            }, 2000);
          } else {
            linkAlertBox.innerHTML = `<div class="alert alert-success" role="alert">
                        <i class="dripicons-checkmark me-2"></i><strong>success</strong>. This booking has been updated
                                                </div>`;
            setTimeout(() => {
              $("#new-task-modal").modal("hide");
              linkAlertBox.innerHTML = "";
              window.location.reload();
            }, 2000);
          }
        },
        error: function (error) {
          linkSpinnerBox.innerHTML = "";
          linkAlertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                            <i class="dripicons-wrong me-2"></i> <strong>Ups</strong>.Something went wrong.
                        </div>`;
          setTimeout(() => {
            $("#add-task-modal").modal("hide");
            linkAlertBox.innerHTML = "";
          }, 2000);
        },
      });
    } else {
      linkInput.classList.remove("is-valid");
      linkInput.classList.add("is-invalid");
    }
  });
}

$(document).ready(function () {
  // $.fn.dataTable.moment("DD/MM/YYYY, hh:mm")
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
      { orderable: !1 },
      { orderable: !1 },
      { orderable: !1 },
      //   { orderable: !1 },
    ],
    order: false,
    select: { style: "multi" },
    drawCallback: function () {
      $(".dataTables_paginate > .pagination").addClass("pagination-rounded"),
        $("#tasks-datatable_length label").addClass("form-label");
    },
  });
});

finishForm.addEventListener("submit", (e) => {
  e.preventDefault();
  spinnerBox.innerHTML = '<div class="spinner-border" role="status"></div>';
  $.ajax({
    type: "POST",
    url: `/${taskId}/finish/`,
    data: {
      csrfmiddlewaretoken: csrf[0].value,
      task: taskId,
    },
    success: function (response) {
      spinnerBox.innerHTML = "";
      if (response.status === "finished") {
        alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                  <i class="dripicons-checkmark me-2"></i><strong>success</strong>. Your booking has been finished
                  </div>`;
        setTimeout(() => {
          $("#finish-task-modal").modal("toggle");
          alertBox.innerHTML = "";
          window.location.reload();
        }, 2000);
      } else {
        alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                 <i class="dripicons-checkmark me-2"></i><strong>failed</strong>. Your booking are in date yet
                                           </div>`;
        setTimeout(() => {
          $("#finish-task-modal").modal("toggle");
          alertBox.innerHTML = "";
        }, 2000);
      }
    },
    error: function (error) {
      spinnerBox.innerHTML = "";
      alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                  <i class="dripicons-wrong me-2"></i> <strong>Ups</strong>.Something went wrong.
              </div>`;
      setTimeout(() => {
        $("#finish-task-modal").modal("toggle");
        alertBox.innerHTML = "";
      }, 2000);
    },
  });
});
