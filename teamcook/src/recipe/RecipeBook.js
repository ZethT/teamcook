import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  CListGroup,
  CListGroupItem,
  CFormInput,
  CRow,
  CCol,
  CButton,
  CModal,
  CModalHeader,
  CModalBody,
  CModalFooter,
  CAlert,
  CSpinner,
} from '@coreui/react'
import api from '../api'

const RecipeBook = () => {
  const [processedRecipes, setProcessedRecipes] = useState([])
  const [fullRecipes, setFullRecipes] = useState([])
  const [searchQueryProcessed, setSearchQueryProcessed] = useState('')
  const [searchQueryFull, setSearchQueryFull] = useState('')
  const [deleteModal, setDeleteModal] = useState({ show: false, recipe: null })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchRecipes()
  }, [])

  const fetchRecipes = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.get('/recipes/')
      setProcessedRecipes(response.data.filter((recipe) => recipe.type === 'Processed'))
      setFullRecipes(response.data.filter((recipe) => recipe.type === 'Full Recipe'))
    } catch (error) {
      console.error('Error fetching recipes:', error)
      setError('Failed to fetch recipes. Please try again later.')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateNew = (type) => {
    navigate('/recipe-builder', { state: { type } })
  }

  const handleEdit = (recipe) => {
    navigate(`/recipe-builder/${recipe.id}`, { state: { recipe } })
  }

  const handleDelete = async () => {
    try {
      await api.delete(`/recipes/${deleteModal.recipe.id}`)
      setDeleteModal({ show: false, recipe: null })
      fetchRecipes()
    } catch (error) {
      console.error('Error deleting recipe:', error)
      setError('Failed to delete recipe. Please try again later.')
    }
  }

  const RecipeList = ({ recipes, searchQuery, setSearchQuery, type }) => (
    <CCol xs={12} md={6}>
      <div className="d-flex align-items-center mb-3">
        <CFormInput
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="me-2"
        />
        <CButton color="primary" onClick={() => handleCreateNew(type)}>
          Create New
        </CButton>
      </div>
      <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
        <CListGroup>
          {recipes
            .filter((recipe) => recipe.name.toLowerCase().includes(searchQuery.toLowerCase()))
            .map((recipe) => (
              <CListGroupItem key={recipe.id}>
                <div className="d-flex w-100 justify-content-between">
                  <h5 className="mb-1">{recipe.name}</h5>
                  <small>{new Date(recipe.creation_time).toLocaleDateString()}</small>
                </div>
                <p className="mb-1">Type: {recipe.type}</p>
                <div className="d-flex justify-content-end">
                  <CButton
                    color="info"
                    size="sm"
                    className="me-2"
                    onClick={() => handleEdit(recipe)}
                  >
                    Edit
                  </CButton>
                  <CButton
                    color="danger"
                    size="sm"
                    onClick={() => setDeleteModal({ show: true, recipe })}
                  >
                    Delete
                  </CButton>
                </div>
              </CListGroupItem>
            ))}
        </CListGroup>
      </div>
    </CCol>
  )

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <CSpinner color="primary" />
      </div>
    )
  }

  return (
    <>
      <h1 className="mb-4">Recipe Book</h1>
      {error && <CAlert color="danger">{error}</CAlert>}
      <CRow>
        <RecipeList
          recipes={processedRecipes}
          searchQuery={searchQueryProcessed}
          setSearchQuery={setSearchQueryProcessed}
          type="Processed"
        />
        <RecipeList
          recipes={fullRecipes}
          searchQuery={searchQueryFull}
          setSearchQuery={setSearchQueryFull}
          type="Full Recipe"
        />
      </CRow>

      <CModal
        visible={deleteModal.show}
        onClose={() => setDeleteModal({ show: false, recipe: null })}
      >
        <CModalHeader closeButton>Confirm Delete</CModalHeader>
        <CModalBody>
          Are you sure you want to delete the recipe "{deleteModal.recipe?.name}"?
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setDeleteModal({ show: false, recipe: null })}>
            Cancel
          </CButton>
          <CButton color="danger" onClick={handleDelete}>
            Delete
          </CButton>
        </CModalFooter>
      </CModal>
    </>
  )
}

export default RecipeBook
