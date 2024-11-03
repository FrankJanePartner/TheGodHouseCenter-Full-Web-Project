/* toggle memu */
let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.accordion_menu');

menu.onclick = () => {
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

/* window.onscroll = () => {
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
} */
/* toggle memu */

// ACCORDION START
let listElements = document.querySelectorAll('.link');

listElements.forEach(listElement => {
    listElement.addEventListener('click', ()=>{
        if (listElement.classList.contains('active')){
            listElement.classList.remove('active');
        }else{
            listElements.forEach (listE => {
                listE.classList.remove('active');
            })
            listElement.classList.toggle('active');
        }
    })
});
//ACCORDION END
