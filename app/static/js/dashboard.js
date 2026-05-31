async function loadDashboard(report, quality) {

    const totalNulls = report.nulls
        ? Object.values(report.nulls)
            .reduce((a, b) => a + b, 0)
        : 0

    document.getElementById(
        "totalRows"
    ).textContent = report.rows

    document.getElementById(
        "totalColumns"
    ).textContent = report.columns

    document.getElementById(
        "duplicates"
    ).textContent = report.duplicates

    document.getElementById(
        "nullValues"
    ).textContent = totalNulls

    document.getElementById(
        "completeness"
    ).textContent =
        `${quality.completeness}%`

    document.getElementById(
        "uniqueness"
    ).textContent =
        `${quality.uniqueness}%`

    document.getElementById(
        "validity"
    ).textContent =
        `${quality.validity}%`

    updateQualityScore(
        quality.score
    )
}

function updateQualityScore(score) {

    const scoreElement =
        document.getElementById(
            "qualityScore"
        )

    const statusElement =
        document.getElementById(
            "qualityStatus"
        )

    const bar =
        document.getElementById(
            "qualityFill"
        )

    scoreElement.textContent =
        `${score}%`

    bar.style.width =
        `${score}%`

    const card =
        scoreElement.closest(
            ".metric-card"
        )

    card.classList.remove(
        "good",
        "medium",
        "bad"
    )

    if (score >= 90) {

        statusElement.textContent =
            "Excelente qualidade"

        scoreElement.style.color =
            "#22c55e"

        bar.style.background =
            "#22c55e"

        card.classList.add(
            "good"
        )
    }

    else if (score >= 70) {

        statusElement.textContent =
            "Boa qualidade"

        scoreElement.style.color =
            "#f59e0b"

        bar.style.background =
            "#f59e0b"

        card.classList.add(
            "medium"
        )
    }

    else {

        statusElement.textContent =
            "Necessita tratamento"

        scoreElement.style.color =
            "#ef4444"

        bar.style.background =
            "#ef4444"

        card.classList.add(
            "bad"
        )
    }
}