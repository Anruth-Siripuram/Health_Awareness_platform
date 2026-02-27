function calcBMI() {
    const w = parseFloat(document.getElementById("weight").value);
    const h = parseFloat(document.getElementById("height").value)/100;

    if(!w || !h) { 
        document.getElementById("bmi-result").innerText = "Enter valid inputs"; 
        return; 
    }

    const bmi = (w/(h*h)).toFixed(2);
    let category = "";
    let stage = "";

    if(bmi < 18.5) {
        category = "Underweight";
        if(bmi < 15) stage = "Stage 3 (Very severe)";
        else if(bmi < 16) stage = "Stage 2 (Severe)";
        else stage = "Stage 1 (Moderate)";
    } 
    else if(bmi < 25) {
        category = "Normal";
        if(bmi < 20) stage = "Stage 1 (Lower normal)";
        else if(bmi < 23) stage = "Stage 2 (Mid normal)";
        else stage = "Stage 3 (Upper normal)";
    } 
    else if(bmi < 30) {
        category = "Overweight";
        if(bmi < 27.5) stage = "Stage 1 (Pre-obese)";
        else stage = "Stage 2 (High pre-obese)";
    } 
    else {
        category = "Obese";
        if(bmi < 35) stage = "Stage 1 (Obesity class I)";
        else if(bmi < 40) stage = "Stage 2 (Obesity class II)";
        else stage = "Stage 3 (Obesity class III)";
    }

    document.getElementById("bmi-result").innerText = `BMI: ${bmi} (${category}, ${stage})`;
}

// Header scroll effect
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 50) header.classList.add('shrink');
    else header.classList.remove('shrink');
});
