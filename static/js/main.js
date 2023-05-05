// CLOSE ALERT FUNCTION
function closeAlert() {
    var alert = document.querySelector('.alert');
    alert.classList.add('hide-alert')
}


// SHOW OVERLAY IN INVENTORY PAGE WHEN USER CLICKS THE EDIT UNITS BUTTON
const editButtons = document.querySelectorAll('.edit-button');
const overlay = document.querySelector('.overlay');
const overlayContent = document.querySelector('.overlay-content');

editButtons.forEach(button => {
    button.addEventListener('click', (event) => {
        const materialCode = event.target.dataset.materialCode;
        document.querySelector('#material-code').value = materialCode;
        overlay.classList.add('active');
    });
});

overlay.addEventListener('click', (event) => {
    if (event.target == overlay) {
        overlay.classList.remove('active');
    }
});