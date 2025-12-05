
// SEE MORE DROP DOWN
let wraper = document.querySelectorAll('.past_series_item_container');
let btn = document.querySelector('.seriesbtn');

let currentimg = 1; //
btn.addEventListener('click', function () {
    for(let i = currentimg; i < currentimg +1; i++) {  //+2
        if (wraper[i]) {
            wraper[i].style.display = 'flex';
        }
    }

    //currentimg += 1;
    //if (currentimg >= wraper.length) {
   //     event.target.style.display="none";
   // }
}); 

// SEE MORE DROP DOWN END



