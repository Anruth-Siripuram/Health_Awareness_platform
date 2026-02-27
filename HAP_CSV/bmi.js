const readline = require("readline");

function calcBMI(weight, heightCm) {
    const h = heightCm / 100;

    if (weight <= 0 || heightCm <= 0 || isNaN(weight) || isNaN(heightCm)) {
        return "Enter valid inputs";
    }

    const bmi = (weight / (h * h)).toFixed(2);
    let category = "";
    let stage = "";

    if (bmi < 18.5) {
        category = "Underweight";
        if (bmi < 15) stage = "Stage 3 (Very severe)";
        else if (bmi < 16) stage = "Stage 2 (Severe)";
        else stage = "Stage 1 (Moderate)";
    } 
    else if (bmi < 25) {
        category = "Normal";
        if (bmi < 20) stage = "Stage 1 (Lower normal)";
        else if (bmi < 23) stage = "Stage 2 (Mid normal)";
        else stage = "Stage 3 (Upper normal)";
    } 
    else if (bmi < 30) {
        category = "Overweight";
        if (bmi < 27.5) stage = "Stage 1 (Pre-obese)";
        else stage = "Stage 2 (High pre-obese)";
    } 
    else {
        category = "Obese";
        if (bmi < 35) stage = "Stage 1 (Obesity class I)";
        else if (bmi < 40) stage = "Stage 2 (Obesity class II)";
        else stage = "Stage 3 (Obesity class III)";
    }

    return `BMI: ${bmi} (${category}, ${stage})`;
}

// Terminal input interface
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Enter weight (kg): ", w => {
    rl.question("Enter height (cm): ", h => {
        const result = calcBMI(parseFloat(w), parseFloat(h));
        console.log(result);
        rl.close();
    });
});
