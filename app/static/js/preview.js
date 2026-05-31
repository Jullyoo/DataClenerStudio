function renderPreview(data) {

    const preview =
        document.getElementById(
            "preview"
        )

    preview.innerHTML = ""

    if (
        !data ||
        !data.length
    ) {

        preview.innerHTML = `

            <div class="empty-preview">

                Nenhum dado disponível.

            </div>

        `

        return
    }

    const table =
        document.createElement(
            "table"
        )

    const headers =
        Object.keys(data[0])

    let html = ""

    html += `
        <thead>
            <tr>
    `

    headers.forEach(
        header => {

            html += `
                <th>
                    ${header}
                </th>
            `
        }
    )

    html += `
            </tr>
        </thead>
    `

    html += `
        <tbody>
    `

    data.forEach(
        row => {

            html += "<tr>"

            headers.forEach(
                header => {

                    const value =
                        row[header]

                    const isNull =
                        value === null ||
                        value === undefined ||
                        value === ""

                    html += `

                        <td class="${
                            isNull
                                ? "null-cell"
                                : ""
                        }">

                            ${
                                isNull
                                    ? "NULL"
                                    : value
                            }

                        </td>

                    `
                }
            )

            html += "</tr>"
        }
    )

    html += `
        </tbody>
    `

    table.innerHTML =
        html

    const info =
        document.createElement(
            "div"
        )

    info.className =
        "preview-info"

    info.innerHTML = `

        Exibindo

        <strong>
            ${data.length}
        </strong>

        registros

    `

    preview.appendChild(
        info
    )

    preview.appendChild(
        table
    )
}