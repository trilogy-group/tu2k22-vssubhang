const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");

signUpButton.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});


let apiCall = async(url, requestOptions)=> {
    let response = await fetch(url, requestOptions);
    if(response.status == "200")
        alert("Logged in")
    else
        alert("Could not Log in. Try again")
}

let validateRegister = (username, email, password, confirmPassword) => {
    return password == confirmPassword && validateEmail(email);
};

function validateEmail(mail) 
{
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.mail);
  {
    return (true)
  }
    alert("You have entered an invalid email address!")
    return (false)
}

let register = () => {
    const username = document.getElementById("register-name").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const confirmPassword = document.getElementById("register-confirm-password").value;
    console.log(username, email, password, confirmPassword)
    if (!validateRegister(username, email, password, confirmPassword)) {
        return;
    }
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        name: username,
        email: email,
        password: password,
    });

    var requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow",
    };

    url = "https://8000-lime-capybara-6omy6a7p.ws.trilogy.devspaces.com/api/v1/auth/signup/"
    apiCall(url, requestOptions)

    
};

let validateLogin = (email, password) => {
    return 1;
};

let login = () => {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    if (!validateEmail(email)) {
        return;
    }
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "email": email,
        "password": password
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    url = "https://8000-lime-capybara-6omy6a7p.ws.trilogy.devspaces.com/api/v1/auth/login/"
    apiCall(url, requestOptions)
};

const registerButton = document.getElementById("register-button");
const loginButton = document.getElementById("login-button");

registerButton.addEventListener("click", () => {
    register();
});

loginButton.addEventListener("click", () => {
    login();
});