import React, { useState, useEffect } from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CButton,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CForm,
  CFormInput,
  CFormSelect,
} from '@coreui/react'
import api from '../api'

const IngredientManagement = () => {
  const [ingredients, setIngredients] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [currentIngredient, setCurrentIngredient] = useState({})
  const [isEditing, setIsEditing] = useState(false)

  useEffect(() => {
    fetchIngredients()
  }, [])

  const fetchIngredients = async () => {
    try {
      const response = await api.get('/ingredients')
      setIngredients(response.data)
    } catch (error) {
      console.error('Error fetching ingredients:', error)
    }
  }

  const handleAddIngredient = () => {
    setCurrentIngredient({ categories: [] })
    setIsEditing(false)
    setShowModal(true)
  }

  const handleEditIngredient = (ingredient) => {
    setCurrentIngredient({
      ...ingredient,
      categories: ingredient.categories.join(','),
    })
    setIsEditing(true)
    setShowModal(true)
  }

  const handleDeleteIngredient = async (id) => {
    if (window.confirm('Are you sure you want to delete this ingredient?')) {
      try {
        await api.delete(`/ingredients/${id}`)
        fetchIngredients()
      } catch (error) {
        console.error('Error deleting ingredient:', error)
      }
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    try {
      const payload = {
        ...currentIngredient,
        categories: currentIngredient.categories.split(',').map((cat) => cat.trim()),
      }
      if (isEditing) {
        await api.put(`/ingredients/${currentIngredient.id}`, payload)
      } else {
        await api.post('/ingredients', payload)
      }
      setShowModal(false)
      fetchIngredients()
    } catch (error) {
      console.error('Error saving ingredient:', error)
    }
  }

  return (
    <CCard>
      <CCardHeader>
        <h2>Ingredient Management</h2>
        <CButton color="primary" onClick={handleAddIngredient}>
          Add New Ingredient
        </CButton>
      </CCardHeader>
      <CCardBody>
        <CTable striped>
          <CTableHead>
            <CTableRow>
              <CTableHeaderCell>Name</CTableHeaderCell>
              <CTableHeaderCell>Unit</CTableHeaderCell>
              <CTableHeaderCell>Type</CTableHeaderCell>
              <CTableHeaderCell>Categories</CTableHeaderCell>
              <CTableHeaderCell>Actions</CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            {ingredients.map((ingredient) => (
              <CTableRow key={ingredient.id}>
                <CTableDataCell>{ingredient.name}</CTableDataCell>
                <CTableDataCell>{ingredient.unit}</CTableDataCell>
                <CTableDataCell>{ingredient.type}</CTableDataCell>
                <CTableDataCell>{ingredient.categories.join(', ')}</CTableDataCell>
                <CTableDataCell>
                  <CButton
                    color="info"
                    size="sm"
                    className="me-2"
                    onClick={() => handleEditIngredient(ingredient)}
                  >
                    Edit
                  </CButton>
                  <CButton
                    color="danger"
                    size="sm"
                    onClick={() => handleDeleteIngredient(ingredient.id)}
                  >
                    Delete
                  </CButton>
                </CTableDataCell>
              </CTableRow>
            ))}
          </CTableBody>
        </CTable>
      </CCardBody>

      <CModal visible={showModal} onClose={() => setShowModal(false)}>
        <CModalHeader closeButton>
          <CModalTitle>{isEditing ? 'Edit Ingredient' : 'Add New Ingredient'}</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CForm onSubmit={handleSubmit}>
            <CFormInput
              className="mb-3"
              label="Name"
              value={currentIngredient.name || ''}
              onChange={(e) => setCurrentIngredient({ ...currentIngredient, name: e.target.value })}
              required
            />
            <CFormInput
              className="mb-3"
              label="Unit"
              value={currentIngredient.unit || ''}
              onChange={(e) => setCurrentIngredient({ ...currentIngredient, unit: e.target.value })}
              required
            />
            <CFormSelect
              className="mb-3"
              label="Type"
              value={currentIngredient.type || ''}
              onChange={(e) => setCurrentIngredient({ ...currentIngredient, type: e.target.value })}
              required
            >
              <option value="">Select type</option>
              <option value="Raw">Raw</option>
              <option value="Processed">Processed</option>
            </CFormSelect>
            <CFormInput
              className="mb-3"
              label="Categories (comma-separated)"
              value={currentIngredient.categories || ''}
              onChange={(e) =>
                setCurrentIngredient({ ...currentIngredient, categories: e.target.value })
              }
            />
            <CModalFooter>
              <CButton color="secondary" onClick={() => setShowModal(false)}>
                Cancel
              </CButton>
              <CButton color="primary" type="submit">
                {isEditing ? 'Update' : 'Add'}
              </CButton>
            </CModalFooter>
          </CForm>
        </CModalBody>
      </CModal>
    </CCard>
  )
}

export default IngredientManagement
