import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { CWidgetStatsA, CWidgetStatsD, CRow, CCol, CButton } from '@coreui/react'
import { CChartLine } from '@coreui/react-chartjs'
import CIcon from '@coreui/icons-react'
import { cilTruck } from '@coreui/icons'
import api from '../api' // Import the axios instance

const Dashboard = () => {
  const [stockCounts, setStockCounts] = useState({ raw_count: 0, processed_count: 0 })
  const [stockHistory, setStockHistory] = useState({ dates: [], raw_data: [], processed_data: [] })

  useEffect(() => {
    // Fetch stock counts
    api
      .get('/stats/stock_counts')
      .then((response) => {
        setStockCounts(response.data)
      })
      .catch((error) => {
        console.error('Error fetching stock counts:', error)
      })

    // Fetch stock history
    api
      .get('/stats/stock_history')
      .then((response) => {
        setStockHistory(response.data)
      })
      .catch((error) => {
        console.error('Error fetching stock history:', error)
      })
  }, [])

  return (
    <>
      <h1>Welcome to Papa John</h1>
      <CRow>
        <CCol xs={12}>
          <Link to="/inventory" style={{ textDecoration: 'none' }}>
            <CWidgetStatsD
              className="mb-3"
              icon={<CIcon className="my-4 text-white" icon={cilTruck} height={52} />}
              chart={
                <CChartLine
                  className="position-absolute w-100 h-100"
                  data={{
                    labels: stockHistory.dates,
                    datasets: [
                      {
                        label: 'Raw Ingredients',
                        backgroundColor: 'rgba(255,255,255,.1)',
                        borderColor: 'rgba(255,255,255,.55)',
                        pointHoverBackgroundColor: '#fff',
                        borderWidth: 2,
                        data: stockHistory.raw_data,
                        fill: true,
                      },
                      {
                        label: 'Processed Ingredients',
                        backgroundColor: 'rgba(255,255,255,.7)',
                        borderColor: 'rgba(255,255,255,.55)',
                        pointHoverBackgroundColor: '#fff',
                        borderWidth: 2,
                        data: stockHistory.processed_data,
                        fill: true,
                      },
                    ],
                  }}
                  options={{
                    elements: {
                      line: {
                        tension: 0.4,
                      },
                      point: {
                        radius: 0,
                        hitRadius: 10,
                        hoverRadius: 4,
                        hoverBorderWidth: 3,
                      },
                    },
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        display: true,
                        labels: {
                          color: '#fff',
                        },
                      },
                    },
                    scales: {
                      x: {
                        display: false,
                      },
                      y: {
                        display: false,
                      },
                    },
                  }}
                />
              }
              style={{ '--cui-card-cap-bg': '#3b5998' }}
              values={[
                { title: 'Raw Ingredients', value: stockCounts.raw_count },
                { title: 'Processed Ingredients', value: stockCounts.processed_count },
              ]}
            />
          </Link>
        </CCol>
      </CRow>
      <CRow>
        <CCol sm={4}>
          <CWidgetStatsA
            className="mb-4"
            color="primary"
            value={<>Recipe Book</>}
            action={
              <Link to="/recipe-book" style={{ textDecoration: 'none' }}>
                <CButton color="light">Go</CButton>
              </Link>
            }
            chart={
              <CChartLine
                className="mt-3 mx-3"
                style={{ height: '90px' }}
                data={{
                  labels: ['x'],
                }}
              />
            }
          />
        </CCol>
        <CCol sm={4}>
          <CWidgetStatsA
            className="mb-4"
            color="success"
            value={<>Budget</>}
            action={
              <Link to="/budget" style={{ textDecoration: 'none' }}>
                <CButton color="light">Go</CButton>
              </Link>
            }
            chart={
              <CChartLine
                className="mt-3 mx-3"
                style={{ height: '90px' }}
                data={{
                  labels: ['x'],
                }}
              />
            }
          />
        </CCol>
        <CCol sm={4}>
          <CWidgetStatsA
            className="mb-4"
            color="info"
            value={<>Calendar</>}
            action={
              <Link to="/calendar" style={{ textDecoration: 'none' }}>
                <CButton color="light">Go</CButton>
              </Link>
            }
            chart={
              <CChartLine
                className="mt-3 mx-3"
                style={{ height: '90px' }}
                data={{
                  labels: ['x'],
                }}
              />
            }
          />
        </CCol>
        <CCol sm={12}>
          <CWidgetStatsA
            className="mb-4"
            color="warning"
            value={<>Team</>}
            action={
              <Link to="/team" style={{ textDecoration: 'none' }}>
                <CButton color="light">Go</CButton>
              </Link>
            }
            chart={
              <CChartLine
                className="mt-3"
                style={{ height: '90px' }}
                data={{
                  labels: ['x'],
                }}
              />
            }
          />
        </CCol>
      </CRow>
    </>
  )
}

export default Dashboard
