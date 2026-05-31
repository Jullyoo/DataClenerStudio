async function uploadFile() {

    const fileInput =
        document.getElementById(
            "fileInput"
        )

    if (!fileInput.files.length) {

        showToast(
            "Selecione um arquivo."
        )

        return
    }

    const formData =
        new FormData()

    formData.append(
        "file",
        fileInput.files[0]
    )

    try {

        const response =
            await fetch(
                "/upload",
                {
                    method: "POST",
                    body: formData
                }
            )

        if (!response.ok) {

            throw new Error(
                "Erro ao processar arquivo."
            )
        }

        const data =
            await response.json()

        console.log(data)

        loadDashboard(
            data.profile,
            data.quality
        )

        renderPreview(
            data.preview
        )

        pipeline.length = 0

        document.getElementById(
            "pipeline"
        ).innerHTML = ""

        data.history.forEach(
            step => {

                addNode(
                    step.action
                )

            }
        )

        const results =
            document.getElementById(
                "results"
            )

        results.classList.remove(
            "hidden"
        )

        document.getElementById(
            "resultMessage"
        ).textContent =
            data.message

        document
            .getElementById(
                "exportSection"
            )
            .classList.remove(
                "hidden"
            )
        showToast(
            "Dataset processado com sucesso."
        )

    }

    catch (error) {

        console.error(
            error
        )

        showToast(
            "Erro ao processar arquivo."
        )
    }
}

function showToast(message) {

    const toast =
        document.getElementById(
            "toast"
        )

    toast.textContent =
        message

    toast.classList.add(
        "show"
    )

    setTimeout(() => {

        toast.classList.remove(
            "show"
        )

    }, 3000)
}

document
    .getElementById(
        "fileInput"
    )
    .addEventListener(
        "change",
        function () {

            const file =
                this.files[0]

            if (!file) return

            const label =
                document.querySelector(
                    ".upload-box span"
                )

            label.textContent =
                file.name
        }
    )