import React, { useState, useEffect } from 'react'
import {
  CButton,
  CTable,
  CTableBody,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CTableDataCell,
  CCard,
  CCardBody,
  CCardHeader,
  CPagination,
  CPaginationItem,
  CFormSelect,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CBadge,
  CAlert,
} from '@coreui/react'
import { useNavigate } from 'react-router-dom'
import api from '../api'

const StockList = () => {
  const [stocks, setStocks] = useState([])
  const [groupedStocks, setGroupedStocks] = useState([])
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(10)
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [showLogModal, setShowLogModal] = useState(false)
  const [logData, setLogData] = useState([])
  const [selectedIngredient, setSelectedIngredient] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await api.get('/stocks/')
        setStocks(response.data)
        setError(null) // Clear any previous errors
      } catch (error) {
        console.error('Error fetching stocks:', error)
        setError('Failed to fetch stocks. Please try again later.')
      } finally {
        setLoading(false)
      }
    }
    fetchStocks()
  }, [])

  useEffect(() => {
    const groupStocksByIngredient = () => {
      const grouped = {}

      stocks.forEach((stock) => {
        const ingredientName = stock.ingredient_name
        const unit = stock.unit

        if (!grouped[ingredientName]) {
          grouped[ingredientName] = {
            ingredient_name: ingredientName,
            total_amount: 0,
            unit: unit,
          }
        }

        grouped[ingredientName].total_amount += parseFloat(stock.amount)
      })

      const groupedArray = Object.values(grouped)
      setGroupedStocks(groupedArray)
    }

    groupStocksByIngredient()
  }, [stocks])

  // Pagination logic
  const indexOfLastStock = currentPage * itemsPerPage
  const indexOfFirstStock = indexOfLastStock - itemsPerPage
  const currentStocks = groupedStocks.slice(indexOfFirstStock, indexOfLastStock)

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  const handleItemsPerPageChange = (event) => {
    setItemsPerPage(Number(event.target.value))
    setCurrentPage(1)
  }

  const handleView = async (ingredientName) => {
    setSelectedIngredient(ingredientName)
    try {
      const response = await api.get(`/stocks/log/${encodeURIComponent(ingredientName)}`)
      setLogData(response.data)
      setShowLogModal(true)
    } catch (error) {
      console.error('Error fetching stock log:', error)
      setError('Failed to fetch stock log. Please try again later.')
    }
  }

  const closeLogModal = () => {
    setShowLogModal(false)
    setLogData([])
    setSelectedIngredient(null)
  }

  const getActionColor = (type) => {
    switch (type) {
      case 'Stock Added':
        return 'success'
      case 'Consumed (Processed Recipe)':
      case 'Consumed (Full Recipe)':
        return 'warning'
      case 'Expired/Wasted':
        return 'danger'
      default:
        return 'info'
    }
  }

  return (
    <>
      <CCard>
        <CCardHeader>Stock List</CCardHeader>
        <CCardBody>
          {error && <CAlert color="danger">{error}</CAlert>}
          <CTable hover responsive>
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell>Ingredient Name</CTableHeaderCell>
                <CTableHeaderCell>Total Amount</CTableHeaderCell>
                <CTableHeaderCell>Unit</CTableHeaderCell>
                <CTableHeaderCell>Actions</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              {loading ? (
                <CTableRow>
                  <CTableDataCell colSpan="4" className="text-center">
                    Loading...
                  </CTableDataCell>
                </CTableRow>
              ) : currentStocks.length > 0 ? (
                currentStocks.map((stock) => (
                  <CTableRow key={stock.ingredient_name}>
                    <CTableDataCell>{stock.ingredient_name}</CTableDataCell>
                    <CTableDataCell>{stock.total_amount.toFixed(2)}</CTableDataCell>
                    <CTableDataCell>{stock.unit}</CTableDataCell>
                    <CTableDataCell>
                      <CButton
                        color="info"
                        size="sm"
                        onClick={() => handleView(stock.ingredient_name)}
                      >
                        View Log
                      </CButton>
                    </CTableDataCell>
                  </CTableRow>
                ))
              ) : (
                <CTableRow>
                  <CTableDataCell colSpan="4" className="text-center">
                    No stocks available.
                  </CTableDataCell>
                </CTableRow>
              )}
            </CTableBody>
          </CTable>
          <div className="d-flex justify-content-between align-items-center mt-3">
            <CFormSelect
              aria-label="Items per page"
              onChange={handleItemsPerPageChange}
              value={itemsPerPage}
              options={[
                { label: '10 items per page', value: 10 },
                { label: '15 items per page', value: 15 },
                { label: '20 items per page', value: 20 },
              ]}
              style={{ width: 'auto' }}
            />
            <CPagination aria-label="Page navigation example">
              <CPaginationItem
                aria-label="Previous"
                disabled={currentPage === 1}
                onClick={() => handlePageChange(currentPage - 1)}
              >
                <span aria-hidden="true">&laquo;</span>
              </CPaginationItem>
              {Array.from(
                { length: Math.ceil(groupedStocks.length / itemsPerPage) },
                (_, index) => (
                  <CPaginationItem
                    key={index + 1}
                    active={index + 1 === currentPage}
                    onClick={() => handlePageChange(index + 1)}
                  >
                    {index + 1}
                  </CPaginationItem>
                ),
              )}
              <CPaginationItem
                aria-label="Next"
                disabled={currentPage === Math.ceil(groupedStocks.length / itemsPerPage)}
                onClick={() => handlePageChange(currentPage + 1)}
              >
                <span aria-hidden="true">&raquo;</span>
              </CPaginationItem>
            </CPagination>
          </div>
        </CCardBody>
      </CCard>

      <CModal visible={showLogModal} onClose={closeLogModal} size="lg">
        <CModalHeader>
          <CModalTitle>Stock Log for {selectedIngredient}</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CTable striped>
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell>Date</CTableHeaderCell>
                <CTableHeaderCell>Action</CTableHeaderCell>
                <CTableHeaderCell>Amount</CTableHeaderCell>
                <CTableHeaderCell>Details</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              {logData.map((entry, index) => (
                <CTableRow key={index}>
                  <CTableDataCell>{new Date(entry.date).toLocaleString()}</CTableDataCell>
                  <CTableDataCell>
                    <CBadge color={getActionColor(entry.type)}>{entry.type}</CBadge>
                  </CTableDataCell>
                  <CTableDataCell>
                    {entry.amount !== undefined ? `${entry.amount} ${entry.unit}` : 'N/A'}
                  </CTableDataCell>
                  <CTableDataCell>{entry.details || entry.reason || 'N/A'}</CTableDataCell>
                </CTableRow>
              ))}
            </CTableBody>
          </CTable>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={closeLogModal}>
            Close
          </CButton>
        </CModalFooter>
      </CModal>
    </>
  )
}

export default StockList
