document.addEventListener("DOMContentLoaded", function() {
  // select initialization
  let selects = document.querySelectorAll("select");
  M.FormSelect.init(selects);

  // dropdown initialization
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems);

  // create const for lash and brow info
  const lashTypeSelect = document.getElementById('lash_type');
  const lashNotesTextarea = document.getElementById('lash_notes');
  const browTypeSelect = document.getElementById('brow_type');
  const browNotesTextarea = document.getElementById('brow_notes');

  // Disable the lash notes textarea initially
  if (lashNotesTextarea !== null) {
    lashNotesTextarea.disabled = true;
  }
  if (browNotesTextarea !== null) {
    browNotesTextarea.disabled = true;
  }

  // Enable or disable lash notes box
  if (lashTypeSelect !== null && lashNotesTextarea !== null) {
    lashTypeSelect.addEventListener('change', function() {
      lashNotesTextarea.disabled = lashTypeSelect.value === '';
    });
  }

  // Enable or disable brow notes box
  if (browTypeSelect !== null && browNotesTextarea !== null) {
    browTypeSelect.addEventListener('change', function() {
      browNotesTextarea.disabled = browTypeSelect.value === '';
    });
  }
});
