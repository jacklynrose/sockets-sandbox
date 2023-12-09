let appState = {}

document.addEventListener('DOMContentLoaded', async () => {
    // initialise state
    await getState()

    const powerEl = document.getElementsByName('power')[0]
    const modeAutoEl = document.getElementById('mode-auto')
    const modeCoolEl = document.getElementById('mode-cool')
    const modeHeatEl = document.getElementById('mode-heat')
    const tempRangeEl = document.getElementsByName('temperature')[0]
    const tempDisplayEl = document.getElementById('temp-display')
    const fanLowEl = document.getElementById('fan-low')
    const fanMedEl = document.getElementById('fan-med')
    const fanHighEl = document.getElementById('fan-high')
    const swingHorizontal = document.getElementById('swing-horizontal')
    const swingVertical = document.getElementById('swing-vertical')
    const timerTypeRadioButtons = document.getElementsByName('timer-type')
    const timerMinutes = document.getElementsByName('timer-minutes')[0]
    const setTimerButton = document.getElementsByName('timer-active')[0]
    const lastTimerSet = document.getElementById('last-timer-set')
    const timerStartAfter = document.getElementById('timer-start-after')
    const timerEndAfter = document.getElementById('timer-end-after')

    render()

    async function getState() {
        appState = await (await fetch('/get')).json()
        console.log(appState)
    }

    async function setState(name, value) {
        await fetch(`/set/${name}${value ? '/' : ''}${value}`)
        await getState()
    }

    function render() {
        powerEl.checked = appState.power === "on"

        modeAutoEl.classList.remove("outline")
        if (appState.mode !== "auto") {
            modeAutoEl.classList.add("outline")
        }

        modeCoolEl.classList.remove("outline")
        if (appState.mode !== "cool") {
            modeCoolEl.classList.add("outline")
        }

        modeHeatEl.classList.remove("outline")
        if (appState.mode !== "heat") {
            modeHeatEl.classList.add("outline")
        }

        tempRangeEl.value = Number(appState.temp)
        tempDisplayEl.value = Number(appState.temp)

        fanLowEl.classList.remove("outline")
        if (appState.fan !== "0") {
            fanLowEl.classList.add("outline")
        }

        fanMedEl.classList.remove("outline")
        if (appState.fan !== "1") {
            fanMedEl.classList.add("outline")
        }

        fanHighEl.classList.remove("outline")
        if (appState.fan !== "2") {
            fanHighEl.classList.add("outline")
        }

        swingHorizontal.classList.remove('outline')
        if (appState.swing === "off" || appState.swing === "vertical") {
            swingHorizontal.classList.add('outline')
        }

        swingVertical.classList.remove('outline')
        if (appState.swing === "off" || appState.swing === "horizontal") {
            swingVertical.classList.add('outline')
        }

        lastTimerSet.classList.remove('hidden')
        if (appState.timerStartAt) {
            lastTimerSet.innerHTML = `Last timer set at ${new Date(appState.timerStartAt)}`
        } else {
            lastTimerSet.classList.add('hidden')
        }

        if (appState.timerType === 'start') {
            timerStartAfter.checked = true
        } else if (appState.timerType === 'end') {
            timerEndAfter.checked = true
        } else {
            timerStartAfter.checked = false
            timerEndAfter.checked = false
        }

        if (appState.durationInMinutes) {
            timerMinutes.value = Number(appState.durationInMinutes)
        } else {
            timerMinutes.value = undefined
        }

        if (appState.timerActive === "true") {
            setTimerButton.checked = true
        } else {
            setTimerButton.checked = false
        }
    }

    powerEl.addEventListener('change', async () => {
        await setState("power", powerEl.checked ? "on" : "off")
        render()
    })

    modeAutoEl.addEventListener('click', async () => {
        await setState("mode", "auto")
        render()
    })

    modeCoolEl.addEventListener('click', async () => {
        await setState("mode", "cool")
        render()
    })

    modeHeatEl.addEventListener('click', async () => {
        await setState("mode", "heat")
        render()
    })

    tempRangeEl.addEventListener('change', async () => {
        await setState("temp", `${tempRangeEl.value}`)
        render()
    })

    fanLowEl.addEventListener('click', async () => {
        await setState("fan", "0")
        render()
    })

    fanMedEl.addEventListener('click', async () => {
        await setState("fan", "1")
        render()
    })

    fanHighEl.addEventListener('click', async () => {
        await setState("fan", "2")
        render()
    })

    swingHorizontal.addEventListener('click', async () => {
        if (appState.swing === "both") {
            await setState("swing", "vertical")
        } else if (appState.swing === "horizontal") {
            await setState("swing", "off")
        } else if (appState.swing === "vertical") {
            await setState("swing", "both")
        } else if (appState.swing === "off") {
            await setState("swing", "horizontal")
        }

        render()
    })

    swingVertical.addEventListener('click', async () => {
        if (appState.swing === "both") {
            await setState("swing", "horizontal")
        } else if (appState.swing === "horizontal") {
            await setState("swing", "both")
        } else if (appState.swing === "vertical") {
            await setState("swing", "off")
        } else if (appState.swing === "off") {
            await setState("swing", "vertical")
        }

        render()
    })

    setTimerButton.addEventListener('click', async () => {
        if (setTimerButton.checked) {
            await setState("durationInMinutes", String(timerMinutes.value))
            await setState("timerType", [...timerTypeRadioButtons].reduce((acc, typeRadio) => {
                return typeRadio.checked ? typeRadio.value : acc
        }, ""))
            await setState("timerStartAt", new Date().toISOString())
            await setState("timerActive", "true")
        } else {
            await setState("durationInMinutes", "")
            await setState("timerType", "")
            await setState("timerStartAt", "")
            await setState("timerActive", "false")
        }
        

        render()
    })
})