function initDashboard(d3, moment) {
    getChargeSummary();

    const form = document.querySelector('form');
    form.addEventListener('submit', event => {
        event.preventDefault();
        getChargeSummary(Array
            .from(form.elements["project"])
            .filter(element => element.checked)
            .map(element => Number(element.value)));
    });

    function getChargeSummary(project_ids = []) {
        fetch(`/admin/monthly-summary?${project_ids.map(project_id => `project=${project_id}`).join('&')}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                renderChargeSummary(data);
                window.addEventListener('resize', () => {
                    renderChargeSummary(data);
                });
            });
    }

    function renderChargeSummary(data) {
        const totalHoursCharged = data
            .map(project => project.total_time_charged)
            .reduce((accumulator, project_hours) => accumulator + moment.duration(project_hours).asHours(), 0);

        // Element selections
        const pageContainer = document.querySelector('#content');
        const chartContainer = document.querySelector('#monthly-charge-summary');
        const svg = d3.select('#monthly-charge-summary > svg');

        // Get necessary height subtractions (to assist in sizing the SVG to the full page height)
        const pageWrapperComputedStyle = window.getComputedStyle(pageContainer, null);
        const containerPaddingTop = Number.parseInt(pageWrapperComputedStyle.getPropertyValue('padding-top'), 10);
        const containerPaddingBottom = Number.parseInt(pageWrapperComputedStyle.getPropertyValue('padding-bottom'), 10);
        const FOOTER_SUBTRACTION = 20;

        // Clear any leftover contents from a previous render
        svg.selectAll('*').remove()

        // Size SVG to use all remaining page space
        const width = chartContainer.clientWidth;
        const height = document.body.clientHeight - chartContainer.offsetTop - containerPaddingTop - containerPaddingBottom - FOOTER_SUBTRACTION;

        svg
            .attr('width', width)
            .attr('height', height);

        // Center chart within SVG
        const container = svg.append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);

        // Create a map of project names to hours spent
        const dataset = data.reduce((map, project) => ({
            ...map,
            [project.project_name]: moment.duration(project.total_time_charged).asHours()
        }), {});

        // Create an ordinal scale mapping projects to categorical colors
        const color = d3
            .scaleOrdinal()
            .domain(dataset)
            .range(d3.schemeCategory10);

        // Create the chart
        const pie = d3
            .pie()
            .value(d => d.value);

        const arc = d3
            .arc()
            .innerRadius(0)
            .outerRadius(Math.min(width / 2, height / 2));

        const slice = container.selectAll('.slice')
            .data(pie(d3.entries(dataset)))
            .enter()
            .append('g')

        slice.append('path')
            .attr('d', arc)
            .attr('fill', (_, i) => color(i));

        slice.append('text')
            .attr('transform', d => `translate(${arc.centroid(d)})`)
            .attr('dx', '-5em')
            .attr('dy', '1em')
            .text(d => `${d.data.key}: ${Number((d.data.value / totalHoursCharged) * 100).toFixed(2)}%`)
            .attr('fill', 'white');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initDashboard(window.d3, window.moment);
});
