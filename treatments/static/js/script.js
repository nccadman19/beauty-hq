document.addEventListener("DOMContentLoaded", function() {
  // select initialization
  let selects = document.querySelectorAll("select");
  M.FormSelect.init(selects);

  // dropdown initialization
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems);

  const lashTypeSelect = document.getElementById('lash_type');
  const lashNotesTextarea = document.getElementById('lash_notes');
  const browTypeSelect = document.getElementById('brow_type');
  const browNotesTextarea = document.getElementById('brow_notes');

  // Disable the lash notes textarea initially
  lashNotesTextarea.disabled = true;
  browNotesTextarea.disabled = true;

  lashTypeSelect.addEventListener('change', function() {
      if (lashTypeSelect.value !== '') {
          lashNotesTextarea.disabled = false;
      } else {
          lashNotesTextarea.disabled = true;
      }
  });

  browTypeSelect.addEventListener('change', function() {
      if (browTypeSelect.value !== '') {
          browNotesTextarea.disabled = false;
      } else {
          browNotesTextarea.disabled = true;
      }
  });
});