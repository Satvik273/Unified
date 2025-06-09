function appendToDisplay(value) {
    const display = document.getElementById('display1');
    display.value += value;
}

function clearDisplay() {
    const display = document.getElementById('display1');
    display.value = '';
}

function calculate() {
    const display = document.getElementById('display1');
    try {
        const result = eval(display.value);
        display.value = result;
    } catch (error) {
        display.value = 'Error';
    }
}

function deleteLastCharacter() {
    const display = document.getElementById('display1');
    display.value = display.value.slice(0, -1);
}
 
function sqrt() {
    const display = document.getElementById('display1');
    try {
        const result = Math.sqrt(parseFloat(display.value));
        display.value = result;
    } catch (error) {
        display.value = 'Error';
    }
}

function power() {
    const display = document.getElementById('display1');
    try {
        const result = Math.pow(parseFloat(display.value), 2);
        display.value = result;
    } catch (error) {
        display.value = 'Error';
    }
}

function percentage() {
    const display = document.getElementById('display1');
    try {
        const result = parseFloat(display.value) / 100;
        display.value = result;
    } catch (error) {
        display.value = 'Error';
    }
}

