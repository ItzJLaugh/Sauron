import { useEffect, useRef } from 'react'
import cytoscape from 'cytoscape'

export default function TopologyMap() {
  const containerRef = useRef(null)
  const cyRef = useRef(null)

  useEffect(() => {
    fetch('http://localhost:8000/api/topology')
      .then(r => r.json())
      .then(data => {
        // Convert backend Sigma.js format to Cytoscape format
        const elements = []

        data.nodes.forEach(node => {
          elements.push({
            data: {
              id: node.key,
              label: node.attributes.label,
              color: node.attributes.color,
              nodeSize: node.attributes.size,
            },
            position: {
              x: node.attributes.x * 30,
              y: node.attributes.y * 30,
            },
          })
        })

        data.edges.forEach(edge => {
          elements.push({
            data: {
              id: edge.key,
              source: edge.source,
              target: edge.target,
              color: edge.attributes.color,
            },
          })
        })

        cyRef.current = cytoscape({
          container: containerRef.current,
          elements,
          style: [
            {
              selector: 'node',
              style: {
                'background-color': 'data(color)',
                'label': 'data(label)',
                'color': '#e2e8f0',
                'font-size': '10px',
                'text-valign': 'bottom',
                'text-margin-y': 5,
                'width': 'data(nodeSize)',
                'height': 'data(nodeSize)',
              },
            },
            {
              selector: 'edge',
              style: {
                'line-color': 'data(color)',
                'width': 2,
                'curve-style': 'bezier',
              },
            },
          ],
          layout: { name: 'preset' },
          userZoomingEnabled: true,
          userPanningEnabled: true,
        })
      })
      .catch(err => console.error('Topology fetch failed:', err))

    return () => {
      if (cyRef.current) cyRef.current.destroy()
    }
  }, [])

  return (
    <div className="topology-panel">
      <div className="panel-header">
        <span>Network Topology</span>
      </div>
      <div ref={containerRef} className="topology-container" />
    </div>
  )
}
