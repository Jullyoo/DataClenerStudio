const pipeline = []

function addNode(type) {

    pipeline.push({

        type: type
    })

    renderPipeline()
}

function renderPipeline() {

    const container = document.getElementById(
        'pipeline'
    )

    container.innerHTML = ''

    pipeline.forEach(node => {

        const div = document.createElement('div')

        div.className = 'pipeline-node'

        div.innerText = node.type

        container.appendChild(div)
    })
}