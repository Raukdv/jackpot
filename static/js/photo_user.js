const imgDiv = document.querySelector('.container-rounded');
const img = document.querySelector('#photo');
const file = document.querySelector("#file");
const uploadBtn = document.querySelector('#uploadBtn');

//hover: en container-rounded
imgDiv.addEventListener(`mouseenter`, function () {
    uploadBtn.style.display = "block";
});
//hover fuera del container-rounded
imgDiv.addEventListener(`mouseleave`, function () {
    uploadBtn.style.display = "none";
});
//imagen a escoger
file.addEventListener(`change`, function () {
    const choosedFile = this.files[0];

    if (choosedFile) {
        const reader = new FileReader(); // FileReader funcion predeterminada de JS
        reader.addEventListener('load', function () {
            img.setAttribute('src', reader.result)
        });
        reader.readAsDataURL(choosedFile);
        //chequea el explorador de archivos
    }
});

