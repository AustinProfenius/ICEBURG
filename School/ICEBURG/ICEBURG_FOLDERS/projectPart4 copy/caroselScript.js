const leftBtn = document.querySelector(".left");
const rightBtn = document.querySelector(".right");

const carouselItems = Array.from(document.querySelectorAll('.carousel-item'));
const navItems = Array.from(document.querySelectorAll('.nav-item'));
const carouselSize = carouselItems.length;


leftBtn.addEventListener('click', swipe);
rightBtn.addEventListener('click', swipe);

function swipe(e){
    const currentCarouselItem = document.querySelector('.carousel-item.active');
    const currentIndex = carouselItems.indexOf(currentCarouselItem);

    let nextIndex;

    if(e.currentTarget.classList.contains('left')){
        if(currentIndex === 0){
            nextIndex = carouselSize - 1;
        }
        else{
            nextIndex = currentIndex - 1;
        }
    }
    else{
        if(currentIndex === carouselSize -1){
            nextIndex = 0;
        }
        else{
            nextIndex = currentIndex + 1;
        }
    }

    carouselItems[nextIndex].classList.add('active');
    navItems[nextIndex].classList.add('active');
    currentCarouselItem.classList.remove('active');
    navItems[currentIndex].classList.remove('active');
}

const nav1 = navItems[0];
const nav2 = navItems[1];
const nav3 = navItems[2];
const nav4 = navItems[3];
const nav5 = navItems[4];

nav1.addEventListener('click', change1);
nav2.addEventListener('click', change2);
nav3.addEventListener('click', change3);
nav4.addEventListener('click', change4);
nav5.addEventListener('click', change5);


function change1(e){
    if(e.currentTarget.classList.contains('active')){
        
    }
    else{
        const currentCarouselItem = document.querySelector('.carousel-item.active');  /*gets current active pic*/
        const currentIndex = carouselItems.indexOf(currentCarouselItem);

        e.currentTarget.classList.add('active');
        carouselItems[0].classList.add('active');

        currentCarouselItem.classList.remove('active');
        navItems[currentIndex].classList.remove('active');
    }
}

function change2(e){
    if(e.currentTarget.classList.contains('active')){
        
    }
    else{
        const currentCarouselItem = document.querySelector('.carousel-item.active');  /*gets current active pic*/
        const currentIndex = carouselItems.indexOf(currentCarouselItem);

        e.currentTarget.classList.add('active');
        carouselItems[1].classList.add('active');

        currentCarouselItem.classList.remove('active');
        navItems[currentIndex].classList.remove('active');
    }
}

function change3(e){
    if(e.currentTarget.classList.contains('active')){
        
    }
    else{
        const currentCarouselItem = document.querySelector('.carousel-item.active');  /*gets current active pic*/
        const currentIndex = carouselItems.indexOf(currentCarouselItem);

        e.currentTarget.classList.add('active');
        carouselItems[2].classList.add('active');

        currentCarouselItem.classList.remove('active');
        navItems[currentIndex].classList.remove('active');
    }
}

function change4(e){
    if(e.currentTarget.classList.contains('active')){
        
    }
    else{
        const currentCarouselItem = document.querySelector('.carousel-item.active');  /*gets current active pic*/
        const currentIndex = carouselItems.indexOf(currentCarouselItem);

        e.currentTarget.classList.add('active');
        carouselItems[3].classList.add('active');

        currentCarouselItem.classList.remove('active');
        navItems[currentIndex].classList.remove('active');
    }
}

function change5(e){
    if(e.currentTarget.classList.contains('active')){
        
    }
    else{
        const currentCarouselItem = document.querySelector('.carousel-item.active');  /*gets current active pic*/
        const currentIndex = carouselItems.indexOf(currentCarouselItem);

        e.currentTarget.classList.add('active');
        carouselItems[4].classList.add('active');

        currentCarouselItem.classList.remove('active');
        navItems[currentIndex].classList.remove('active');
    }
}