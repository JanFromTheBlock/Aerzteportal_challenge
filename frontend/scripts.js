let Base_url = "http://127.0.0.1:8000/";

function get(suffix) {
  let url = Base_url + "api/" + suffix;

  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  if (suffix == "appointments/") {
    token = localStorage.getItem("token");
    myHeaders.append("Authorization", `Token ${token}`);
  }
  const requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow",
  };
  fetch(url, requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
}

function deleteObject(suffix) {
  let url = Base_url + "api/" + suffix;
  id = document.getElementById(`${suffix}`).value;
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    id: id,
  });

  const requestOptions = {
    method: "DELETE",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  fetch(url, requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
}

function createDoctor() {
  username = document.getElementById("username").value;
  password = document.getElementById("password").value;
  firstname = document.getElementById("firstname").value;
  lastname = document.getElementById("lastname").value;
  title = document.getElementById("title").value;
  speciality = document.getElementById("speciality").value;
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    username: username,
    password: password,
    firstname: firstname,
    lastname: lastname,
    title: title,
    speciality: speciality,
  });

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  fetch("http://127.0.0.1:8000/api/doctors/", requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
}

function createClient() {
  username = document.getElementById("username-client").value;
  password = document.getElementById("password-client").value;
  firstname = document.getElementById("firstname-client").value;
  lastname = document.getElementById("lastname-client").value;
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    username: username,
    password: password,
    firstname: firstname,
    lastname: lastname,
  });

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  fetch("http://127.0.0.1:8000/api/patients/", requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
}

function createAppointment() {
  doctorId = document.getElementById("doctor-id").value;
  clientId = document.getElementById("client-id").value;
  title = document.getElementById("title_app").value;
  description = document.getElementById("description").value;
  date = document.getElementById("date").value;
  token = localStorage.getItem("token");
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", `Token ${token}`);

  const raw = JSON.stringify({
    doctor_id: doctorId,
    client_id: clientId,
    title: title,
    description: description,
    date: date,
  });

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  fetch("http://127.0.0.1:8000/api/appointments/", requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
}

async function login() {
  username = document.getElementById("username-login").value;
  password = document.getElementById("password-login").value;
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    username: username,
    password: password,
  });

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/login/",
      requestOptions
    );
    const result = await response.json();
    console.log(result);

    if (response.ok) {
      localStorage.setItem("token", result.token);
      localStorage.setItem("LoggedIn", "true");
      document.getElementById('logout').classList.remove('d-none');
      document.getElementById('login').classList.add('d-none');
      document.getElementById('appointments').classList.remove('d-none');
    } else {
      console.error("Login fehlgeschlagen:", result);
    }
  } catch (error) {
    console.error("Fehler bei der Anfrage:", error);
  }
}

function logout() {
  localStorage.setItem("token", '');
  localStorage.setItem("LoggedIn", "false");
  document.getElementById('logout').classList.add('d-none');
  document.getElementById('login').classList.remove('d-none');
  document.getElementById('appointments').classList.add('d-none');
}

