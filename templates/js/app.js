// Dropdown menu
document.querySelectorAll('.sidebar-submenu').forEach(e => {
  e.querySelector('.sidebar-menu-dropdown').onclick = (event) => {
    event.preventDefault();
    e.querySelector('.sidebar-menu-dropdown .dropdown-icon').classList.toggle('active');

    let dropdown_content = e.querySelector('.sidebar-menu-dropdown-content');
    let dropdown_content_lis = dropdown_content.querySelectorAll('li');

    let active_height = dropdown_content_lis[0].clientHeight * dropdown_content_lis.length

    dropdown_content.classList.toggle('active')
    dropdown_content.style.height = dropdown_content.classList.contains('active') ? active_height + 'px' : '0';
  }
})

if (get().length == 0) {
  set('off');
}

// Dark Mode Toggle
let darkmode_toggle = document.querySelector('#darkmode-toggle')
darkmode_toggle.onclick = (e) => {
  e.preventDefault();
  document.querySelector('body').classList.toggle('dark')
  darkmode_toggle.querySelector('.darkmode-switch').classList.toggle('active')
  if (get() == 'off') {
    set('on');
  } else {
    set('off');
  }
}

// Dark mode load
window.onload = () => {
  if (get() == 'on') {
    document.querySelector('body').classList.toggle('dark')
    darkmode_toggle.querySelector('.darkmode-switch').classList.toggle('active')
  }
}

// Responsive sidebar
let overlay = document.querySelector('.overlay')
let sidebar = document.querySelector('.sidebar')
const mobileBtns = document.querySelectorAll('.mobile-toggle');

for (let i = 0; i < mobileBtns.length; i++) {
  mobileBtns[i].onclick = () => {
    sidebar.classList.toggle('active')
    overlay.classList.toggle('active')
  }
}

document.querySelector('#sidebar-close').onclick = () => {
  sidebar.classList.toggle('active')
  overlay.classList.toggle('active')
};

// Activate Sidebar Item
let sidebarBtns = document.querySelectorAll('.sidebar-menu > li > a');
const mains = document.querySelectorAll('.main');
for (let i = 0; i < sidebarBtns.length - 2; i++) {
  sidebarBtns[i].onclick = function (e) {
    const mainActive = document.querySelector('.main.active');
    let actived_item = document.querySelector('.sidebar-menu > li > a.active');
    e.preventDefault();
    actived_item.classList.remove('active');
    sidebarBtns[i].classList.add('active');
    mainActive.classList.remove('active');
    mains[i].classList.add('active');
    if (sidebar.classList.contains('active')) {
      sidebar.classList.remove('active')
    }
    if (overlay.classList.contains('active')) {
      overlay.classList.remove('active')
    }
  }
}


function get() {
  return JSON.parse(localStorage.getItem('darkMode')) || [];
}

function set(mode) {
  localStorage.setItem('darkMode', JSON.stringify(mode));
}

// Profile modal
const modalProfile = document.querySelector('.modal');
const profile = document.querySelector('.profile');
const closeModalProfile = document.querySelector('.close-profile');
const userInfoBtn = document.querySelector('.sidebar-user-info');

userInfoBtn.onclick = async (e) => {
  e.preventDefault();
  modalProfile.classList.remove('hide');
  JsLoadingOverlay.show()
  await load_profile();
  JsLoadingOverlay.hide()

}

closeModalProfile.onclick = () => {
  modalProfile.classList.add('hide');
}

profile.onclick = (e) => {
  e.stopImmediatePropagation();
}

modalProfile.onclick = () => {
  console.log(1);
  modalProfile.classList.add('hide');
}