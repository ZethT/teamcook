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
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CForm,
  CFormInput,
  CFormSelect,
  CAlert,
} from '@coreui/react'
import api from '../api'

const Team = () => {
  const [teamMembers, setTeamMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [currentMember, setCurrentMember] = useState(null)
  const [restaurants, setRestaurants] = useState([])

  useEffect(() => {
    fetchTeamMembers()
    fetchRestaurants()
  }, [])

  const fetchTeamMembers = async () => {
    try {
      const response = await api.get('/users/')
      setTeamMembers(response.data)
      setError(null)
    } catch (error) {
      console.error('Error fetching team members:', error)
      setError('Failed to fetch team members. Please try again later.')
    } finally {
      setLoading(false)
    }
  }

  const fetchRestaurants = async () => {
    try {
      const response = await api.get('/restaurants/')
      setRestaurants(response.data)
    } catch (error) {
      console.error('Error fetching restaurants:', error)
    }
  }

  const handleAddMember = () => {
    setCurrentMember(null)
    setShowModal(true)
  }

  const handleEditMember = (member) => {
    setCurrentMember(member)
    setShowModal(true)
  }

  const handleDeleteMember = async (id) => {
    if (window.confirm('Are you sure you want to delete this team member?')) {
      try {
        await api.delete(`/users/${id}`)
        await fetchTeamMembers()
        setError(null)
      } catch (error) {
        console.error('Error deleting team member:', error)
        setError('Failed to delete team member. Please try again later.')
      }
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    const formData = new FormData(event.target)
    const memberData = Object.fromEntries(formData.entries())

    try {
      if (currentMember) {
        await api.put(`/users/${currentMember.id}`, memberData)
      } else {
        await api.post('/users/', memberData)
      }
      await fetchTeamMembers()
      setShowModal(false)
      setError(null)
    } catch (error) {
      console.error('Error saving team member:', error)
      setError('Failed to save team member. Please try again later.')
    }
  }

  return (
    <>
      <CCard>
        <CCardHeader>Team Members</CCardHeader>
        <CCardBody>
          {error && <CAlert color="danger">{error}</CAlert>}
          <CButton color="primary" onClick={handleAddMember} className="mb-3">
            Add Team Member
          </CButton>
          <CTable hover responsive>
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell>Name</CTableHeaderCell>
                <CTableHeaderCell>Login ID</CTableHeaderCell>
                <CTableHeaderCell>Role</CTableHeaderCell>
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
              ) : teamMembers.length > 0 ? (
                teamMembers.map((member) => (
                  <CTableRow key={member.id}>
                    <CTableDataCell>{member.name}</CTableDataCell>
                    <CTableDataCell>{member.login_id}</CTableDataCell>
                    <CTableDataCell>{member.role}</CTableDataCell>
                    <CTableDataCell>
                      <CButton
                        color="info"
                        size="sm"
                        onClick={() => handleEditMember(member)}
                        className="me-2"
                      >
                        Edit
                      </CButton>
                      <CButton
                        color="danger"
                        size="sm"
                        onClick={() => handleDeleteMember(member.id)}
                      >
                        Delete
                      </CButton>
                    </CTableDataCell>
                  </CTableRow>
                ))
              ) : (
                <CTableRow>
                  <CTableDataCell colSpan="4" className="text-center">
                    No team members available.
                  </CTableDataCell>
                </CTableRow>
              )}
            </CTableBody>
          </CTable>
        </CCardBody>
      </CCard>

      <CModal visible={showModal} onClose={() => setShowModal(false)}>
        <CForm onSubmit={handleSubmit}>
          <CModalHeader>
            <CModalTitle>{currentMember ? 'Edit' : 'Add'} Team Member</CModalTitle>
          </CModalHeader>
          <CModalBody>
            <CFormInput
              className="mb-3"
              type="text"
              id="name"
              name="name"
              label="Name"
              defaultValue={currentMember?.name}
              required
            />
            <CFormInput
              className="mb-3"
              type="text"
              id="login_id"
              name="login_id"
              label="Login ID"
              defaultValue={currentMember?.login_id}
              required
            />
            <CFormSelect
              className="mb-3"
              id="role"
              name="role"
              label="Role"
              defaultValue={currentMember?.role}
              required
            >
              <option value="">Select a role</option>
              <option value="Manager">Manager</option>
              <option value="Chef">Chef</option>
              <option value="Waiter">Waiter</option>
            </CFormSelect>
            {!currentMember && (
              <CFormInput
                className="mb-3"
                type="password"
                id="password"
                name="password"
                label="Password"
                required
              />
            )}
          </CModalBody>
          <CModalFooter>
            <CButton color="secondary" onClick={() => setShowModal(false)}>
              Cancel
            </CButton>
            <CButton color="primary" type="submit">
              Save
            </CButton>
          </CModalFooter>
        </CForm>
      </CModal>
    </>
  )
}

export default Team
