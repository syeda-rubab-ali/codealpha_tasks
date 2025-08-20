# codealpha_tasks
Age Calculator to calculate exact your age including months and days by just entering ur birth date . I shared code here 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Age Calculator</title>
  <link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins:wght@400;600&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: "Poppins", sans-serif;
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: url("calculator.png") no-repeat center center/cover; /* 👈 Your PNG image */
    }

    .container {
      background: rgba(255, 255, 255, 0.9); /* white glass effect */
      border-radius: 16px;
      padding: 35px 25px;
      width: 360px;
      text-align: center;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
      animation: fadeIn 0.8s ease-in-out;
    }

  h2 {
  margin-bottom: 20px;
  font-size: 32px;
  font-family: 'Pacifico', cursive; /* Stylish handwritten font */
  letter-spacing: 1px;
  background: linear-gradient(90deg, #000, #444); /* Gradient text */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}


    label {
      font-size: 14px;
      font-weight: 500;
      display: block;
      margin-bottom: 8px;
      color: #444;
      text-align: left;
    }

    input {
      padding: 12px;
      width: 100%;
      margin-bottom: 15px;
      border-radius: 10px;
      border: 1px solid #ccc;
      font-size: 15px;
    }

    input:focus {
      border: 1px solid #333;
      outline: none;
      box-shadow: 0 0 6px rgba(0, 0, 0, 0.25);
    }

    button {
      padding: 12px;
      width: 100%;
      background: #333; /* Professional dark button */
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s ease, background 0.3s ease;
    }

    button:hover {
      background: #111;
      transform: translateY(-2px);
    }

    #result {
      margin-top: 18px;
      font-size: 16px;
      font-weight: 500;
      color: #111;
      opacity: 0;
      transform: translateY(15px);
      transition: all 0.5s ease;
    }

    #result.show {
      opacity: 1;
      transform: translateY(0);
    }

    @keyframes fadeIn {
      from {opacity: 0; transform: scale(0.95);}
      to {opacity: 1; transform: scale(1);}
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Age Calculator</h2>
    <label for="dob">Select Your Date of Birth</label>
    <input type="date" id="dob">
    <button onclick="calculateAge()">Calculate Age</button>
    <p id="result"></p>
  </div>

  <script>
    function calculateAge() {
      let dob = document.getElementById('dob').value;
      let result = document.getElementById('result');

      if (!dob) {
        result.innerHTML = "⚠ Please select your date of birth.";
        result.classList.add("show");
        return;
      }

      let dobDate = new Date(dob);
      let today = new Date();

      let years = today.getFullYear() - dobDate.getFullYear();
      let months = today.getMonth() - dobDate.getMonth();
      let days = today.getDate() - dobDate.getDate();

      if (days < 0) {
        months--;
        let prevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
        days += prevMonth.getDate();
      }

      if (months < 0) {
        years--;
        months += 12;
      }

      result.innerHTML = `🎉 You are <b>${years}</b> years, <b>${months}</b> months, and <b>${days}</b> days old.`;
      result.classList.add("show");
    }
  </script>
</body>
</html>
