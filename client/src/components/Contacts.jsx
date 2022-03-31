import { SearchIcon } from "@chakra-ui/icons";
import {
  Button,
  Center,
  Container,
  Link,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  useDisclosure,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { NewContactForm } from "./ContactForms";

const Contacts = () => {
  const [contacts, setContacts] = useState([]);

  useEffect(() => {
    fetch("/api/contacts")
      .then((response) => response.json())
      .then((json) => setContacts(json));
  }, []);

  return (
    <Container>
      <NewContactForm
        onNewContact={(contact) =>
          setContacts((currentContacts) => [...currentContacts, contact])
        }
      />
      <ContactsTable contacts={contacts} />
    </Container>
  );
};

export const ContactsTable = (contacts) => {
  return (
    <TableContainer>
      <Table>
        <Thead>
          <Tr>
            <Th>Name</Th>
            <Th>Company</Th>
            <Th></Th>
          </Tr>
        </Thead>
        <Tbody>
          {contacts.contacts.length > 0 &&
            contacts.contacts.map((contact, idx) => (
              <Tr key={idx}>
                <Td>{contact.name ? contact.name : "-"}</Td>
                <Td>{contact.company ? contact.company : "-"}</Td>
                <Td>
                  <Link href={`/contacts/${contact.id}`}>
                    <SearchIcon />
                  </Link>
                </Td>
              </Tr>
            ))}
          {contacts.contacts.length === 0 && (
            <Tr>
              <Td colSpan={4} textAlign="center">
                No contacts
              </Td>
            </Tr>
          )}
        </Tbody>
      </Table>
    </TableContainer>
  );
};

export const CreateContactModal = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  function validateNotEmpty(value) {
    let error;
    if (!value) {
      error = "Field required";
    }
    return error;
  }

  function validatePhoneNumber(value) {
    let error;
    const regex = /^0[1-9]([-. ]?[0-9]{2}){4}$/;
    if (!regex.test(value)) {
      error = "Please enter a valid french phone number";
    }
    return error;
  }
  return (
    <>
      <Center m="20px">
        <Button onClick={onOpen}>Add a contact</Button>
      </Center>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Adding a contact</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <NewContactForm />
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default Contacts;
