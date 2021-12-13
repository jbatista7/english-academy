$(function () {
  //   let enableDays = [];

  //   let disabledDays = [];
  // let enableDays = ["2021-11-30"];

  // let disabledDays = ["2021-11-28", "2021-11-29"];

  //   function formatDate(d) {
  //     let day = String(d.getDate());

  //     //add leading zero if day is is single digit

  //     if (day.length == 1) day = "0" + day;

  //     let month = String(d.getMonth() + 1);

  //     //add leading zero if month is is single digit

  //     if (month.length == 1) month = "0" + month;

  //     return d.getFullYear() + "-" + month + "-" + day;
  //   }

  $(".datepicker").datepicker({
    format: "dd/mm/yyyy",
    startDate: "+1d",
    // daysOfWeekDisabled: [],

    // beforeShowDay: function (date) {
    //   let dayNr = date.getDay();

    //   if (dayNr == 0 || dayNr == 6) {
    //     if (enableDays.indexOf(formatDate(date)) >= 0) {
    //       return true;
    //     }

    //     return false;
    //   }

    //   if (disabledDays.indexOf(formatDate(date)) >= 0) {
    //     return false;
    //   }

    //   return true;
    // },
  });
});

//   let date = new Date();
//   // add a day
//   date.setDate(date.getDate() + 1);

//   let date = new Date(Date.now() + 3600 * 1000 * 24);

// let disableDates = ["30-11-2021", "25-11-2021", "23-11-2021", "27-11-2021"]; //disabled custom days
// $(".datepicker").datepicker({
//   startDate: new Date(),
//   format: "dd/mm/yyyy",
//   todayHighlight: true,
//   daysOfWeekDisabled: [0, 6], //disabled weekends
//   beforeShowDay: function (date) {
//     dmy =
//       date.getDate() + "-" + (date.getMonth() + 1) + "-" + date.getFullYear();

//     if (disableDates.indexOf(dmy) != -1) {
//       return false;
//     } else {
//       return true;
//     }
//   },
// });
