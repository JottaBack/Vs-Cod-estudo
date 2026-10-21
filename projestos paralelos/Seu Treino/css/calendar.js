const calendarDays = document.querySelector("#calendar-days");
const calendarMonth = document.querySelector("#calendar-month");
const selectedDateLabel = document.querySelector("#calendar-selected-date");
const calendarStatus = document.querySelector("#calendar-status");
const calendarStorageKey = "focofit-training-records";
const today = new Date();
let selectedDate = toDateKey(today);
let visibleMonth = new Date(today.getFullYear(), today.getMonth(), 1);
let records = {};
let storageAvailable = true;

function toDateKey(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

function formatDate(date) {
    return new Intl.DateTimeFormat("pt-BR", {
        day: "numeric",
        month: "long",
        year: "numeric"
    }).format(date);
}

try {
    const savedRecords = window.localStorage.getItem(calendarStorageKey);
    if (savedRecords) {
        const parsedRecords = JSON.parse(savedRecords);
        if (!parsedRecords || typeof parsedRecords !== "object" || Array.isArray(parsedRecords)) {
            throw new TypeError("Formato inválido para os registros de treino.");
        }
        records = Object.fromEntries(
            Object.entries(parsedRecords).filter(([date, value]) =>
                /^\d{4}-\d{2}-\d{2}$/.test(date) &&
                (value === "trained" || value === "missed")
            )
        );
    }
} catch (error) {
    storageAvailable = false;
    calendarStatus.textContent = "Não foi possível carregar ou salvar os registros deste navegador.";
    console.error("Falha ao acessar os registros de treino.", error);
}

function renderCalendar() {
    const year = visibleMonth.getFullYear();
    const month = visibleMonth.getMonth();
    const firstDay = new Date(year, month, 1);
    const startOffset = (firstDay.getDay() + 6) % 7;
    const todayKey = toDateKey(today);
    const fragment = document.createDocumentFragment();

    calendarMonth.textContent = new Intl.DateTimeFormat("pt-BR", {
        month: "long",
        year: "numeric"
    }).format(visibleMonth);
    selectedDateLabel.textContent = `Dia selecionado: ${formatDate(new Date(
        Number(selectedDate.slice(0, 4)),
        Number(selectedDate.slice(5, 7)) - 1,
        Number(selectedDate.slice(8, 10))
    ))}`;

    for (let index = 0; index < 42; index += 1) {
        const date = new Date(year, month, index - startOffset + 1);
        const dateKey = toDateKey(date);
        const record = records[dateKey];
        const dayButton = document.createElement("button");
        dayButton.type = "button";
        dayButton.className = "calendar-day";
        dayButton.dataset.date = dateKey;
        dayButton.setAttribute("aria-pressed", String(dateKey === selectedDate));
        dayButton.setAttribute("aria-label", `${formatDate(date)}${record ? `, ${record === "trained" ? "treino concluído" : "falta"}` : ""}`);
        dayButton.disabled = dateKey > todayKey;

        const dayNumber = document.createElement("span");
        dayNumber.textContent = String(date.getDate());
        dayButton.append(dayNumber);

        if (date.getMonth() !== month) dayButton.classList.add("is-outside-month");
        if (dateKey === selectedDate) dayButton.classList.add("is-selected");
        if (dateKey === todayKey) dayButton.classList.add("is-today");
        if (record) dayButton.classList.add(`is-${record}`);

        dayButton.addEventListener("click", () => {
            selectedDate = dateKey;
            calendarStatus.textContent = "";
            renderCalendar();
        });
        fragment.append(dayButton);
    }

    calendarDays.replaceChildren(fragment);
    document.querySelectorAll("[data-record]").forEach((button) => {
        button.disabled = selectedDate > todayKey || !storageAvailable;
    });
}

document.querySelector("#previous-month").addEventListener("click", () => {
    visibleMonth = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() - 1, 1);
    renderCalendar();
});

document.querySelector("#next-month").addEventListener("click", () => {
    visibleMonth = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth() + 1, 1);
    renderCalendar();
});

document.querySelectorAll("[data-record]").forEach((button) => {
    button.addEventListener("click", () => {
        const record = button.dataset.record;
        const todayKey = toDateKey(today);
        if (selectedDate > todayKey) {
            calendarStatus.textContent = "Não é possível registrar um treino em uma data futura.";
            return;
        }
        if (record !== "trained" && record !== "missed") {
            calendarStatus.textContent = "Não foi possível identificar o registro escolhido.";
            return;
        }

        const previousRecord = records[selectedDate];
        records[selectedDate] = record;
        try {
            window.localStorage.setItem(calendarStorageKey, JSON.stringify(records));
            calendarStatus.textContent = record === "trained"
                ? "Treino concluído registrado."
                : "Falta registrada.";
            renderCalendar();
        } catch (error) {
            if (previousRecord) {
                records[selectedDate] = previousRecord;
            } else {
                delete records[selectedDate];
            }
            storageAvailable = false;
            calendarStatus.textContent = "Não foi possível salvar o registro neste navegador.";
            console.error("Falha ao salvar o registro de treino.", error);
            renderCalendar();
        }
    });
});

renderCalendar();
