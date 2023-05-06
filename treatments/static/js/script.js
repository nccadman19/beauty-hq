document.addEventListener("DOMContentLoaded", function() {
    // sidenav initialization
    let sidenav = document.querySelectorAll(".sidenav");
    M.Sidenav.init(sidenav);

    // datepicker initialization
    let datepicker = document.querySelectorAll(".datepicker");
    M.Datepicker.init(datepicker, {
        format: "dd mmmm, yyyy",
        i18n: {done: "Select"}
    });

    // select initialization
    let selects = document.querySelectorAll("select");
    M.FormSelect.init(selects);

    // collapsible initializataion
    let collapsibles = document.querySelectorAll(".collapsible");
    M.Collapsible.init(collapsibles);
});

// // Get the HTML elements for the dropdown menus
// const treatmentTypeSelect = document.getElementById("treatment-type");
// const lashTypeDiv = document.getElementById("lashes-options");
// const browTypeDiv = document.getElementById("brows-options");
// const bothTypeDiv = document.getElementById("both-options");

// // Hide the "Lash Type" and "Brow Type" dropdown menus initially
// lashTypeDiv.style.display = "none";
// browTypeDiv.style.display = "none";
// bothTypeDiv.style.display = "none";

// // Add an event listener to the "Treatment Type" dropdown menu
// treatmentTypeSelect.addEventListener("change", function() {
//   // Get the selected value from the "Treatment Type" dropdown menu
//   const selectedValue = this.value;

//   // If the selected value is "Lashes", show the "Lash Type" dropdown menu and hide the "Brow Type" dropdown menu
//   if (selectedValue === "L") {
//     lashTypeDiv.style.display = "block";
//     browTypeDiv.style.display = "none";
//     bothTypeDiv.style.display = "none";
//   }
//   // If the selected value is "Brows", show the "Brow Type" dropdown menu and hide the "Lash Type" dropdown menu
//   else if (selectedValue === "B") {
//     lashTypeDiv.style.display = "none";
//     browTypeDiv.style.display = "block";
//     bothTypeDiv.style.display = "none";
//   }
//   // If the selected value is "Both", show both the "Lash Type" and "Brow Type" dropdown menus
//   else if (selectedValue === "BL") {
//     lashTypeDiv.style.display = "block";
//     browTypeDiv.style.display = "block";
//     bothTypeDiv.style.display = "block";
//   }
//   // If none of the above conditions are met, hide both the "Lash Type" and "Brow Type" dropdown menus
//   else {
//     lashTypeDiv.style.display = "none";
//     browTypeDiv.style.display = "none";
//     bothTypeDiv.style.display = "none";
//   }
// });
