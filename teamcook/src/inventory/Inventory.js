import { CCard, CCardBody, CCol, CRow, CAlert } from '@coreui/react'
import React, { useEffect, useState } from 'react'
import api from '../api'
import StockList from './StockList'
import { CChart } from '@coreui/react-chartjs'

const DoughnutChart = ({ rawCount, processedCount }) => {
  const [chartData, setChartData] = useState(null)

  useEffect(() => {
    const totalItems = rawCount + processedCount

    const newChartData = {
      labels: ['Raw', 'Processed'],
      datasets: [
        {
          backgroundColor: ['#41B883', '#E46651'],
          data: [rawCount, processedCount],
        },
      ],
    }

    const options = {
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
        },
      },
    }

    const plugins = [
      {
        id: 'centerText',
        beforeDraw: (chart) => {
          const width = chart.width
          const height = chart.height
          const ctx = chart.ctx

          ctx.restore()
          const fontSize = (height / 170).toFixed(2)
          ctx.font = fontSize + 'em sans-serif'
          ctx.textBaseline = 'middle'

          const text = `Total: ${totalItems}`
          const textX = Math.round((width - ctx.measureText(text).width) / 2)
          const textY = height / 2

          ctx.fillText(text, textX, textY)
          ctx.save()
        },
      },
    ]

    setChartData({ data: newChartData, options, plugins })
  }, [rawCount, processedCount])

  if (!chartData) return null

  return (
    <CChart
      type="doughnut"
      data={chartData.data}
      options={chartData.options}
      plugins={chartData.plugins}
      style={{ height: '300px' }}
    />
  )
}

const Inventory = () => {
  const [stockCounts, setStockCounts] = useState({ raw_count: 0, processed_count: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch stock counts
    api
      .get('/stats/stock_counts')
      .then((response) => {
        setStockCounts(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.error('Error fetching stock counts:', error)
        setLoading(false)
      })
  }, [])

  return (
    <>
      <h1>Papa John Inventory</h1>
      <CRow>
        <CCol xs={6}>
          <CCard className="mb-4">
            <CCardBody>
              {loading ? (
                <p>Loading...</p>
              ) : (
                <DoughnutChart
                  rawCount={stockCounts.raw_count}
                  processedCount={stockCounts.processed_count}
                />
              )}
            </CCardBody>
          </CCard>
        </CCol>
        <CCol xs={6}>
          <CCard className="mb-4">
            <CCardBody>
              <CAlert color="danger" dismissible>
                <strong>Significantly low!</strong> Potato
              </CAlert>
              <CAlert color="warning" dismissible>
                <strong>Low!</strong> Tomato
              </CAlert>
              <CAlert color="warning" dismissible>
                <strong>Low!</strong> Tomato
              </CAlert>
              <CAlert color="warning" dismissible>
                <strong>Low!</strong> Tomato
              </CAlert>
              <CAlert color="warning" dismissible>
                <strong>Low!</strong> Tomato
              </CAlert>
              <CAlert color="warning" dismissible>
                <strong>Low!</strong> Tomato
              </CAlert>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
      <CRow>
        <CCol sm={12}>
          <StockList />
        </CCol>
      </CRow>
    </>
  )
}

export default Inventory