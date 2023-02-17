import React from 'react'
import axios from 'axios';
import { useEffect, useState } from 'react';
import bcrypt from "bcryptjs"
import { useNavigate } from "react-router-dom";

import {
    Table,
    Thead,
    Tbody,
    Tfoot,
    Tr,
    Th,
    Td,
    TableCaption,
    TableContainer,
    Container,
    Text,
    Heading,
    Button,
    ButtonGroup,
    IconButton,
    useToast
} from '@chakra-ui/react'
import NavBar from '../components/Navbar';
const AddEmployees = () => {

    const navigate = useNavigate();
    const toast = useToast();
    const [data, setData] = useState([])
    useEffect(() => {
        let login = localStorage.getItem('login');
        let key = localStorage.getItem('key');
        let key1 = localStorage.getItem('key1');

        let fetchData = async () => {
            try {
                const res = await axios.get('http://localhost:4000/getrequestemployeedetails')
                setData(res.data)
            } catch (err) {
                console.log(err);
                return 0;
            }
        };
        fetchData();
    }, []);
    console.log(data)
    const myArray1 = data


    //button handle
    const handleSubmit = async (userid) => {
        // e.preventDefault();
        let inputs = {
            userid: userid
        }
        try {
            const res = await axios.post("http://localhost:4000/addEmployee", inputs);
            window.location.reload(false);
        } catch (err) {
            console.log(err)
        }
    };

    const handleSubmit1 = async (userid) => {
        // e.preventDefault();
        let inputs = {
            userid: userid
        }
        try {
            const res = await axios.post("http://localhost:4000/removerequestemployee", inputs);
            window.location.reload(false);
        } catch (err) {
            console.log(err)
        }
    };

    return (
        <Container maxW={"100%"} display={"flex"} flexDir="column" padding='0px'>
            <NavBar navItems={NAV_ITEMS} />
        <TableContainer width={"90%"} margin={"auto"} mt={"5vh"}>
            <Table variant='striped'>

                <Thead>
                    <Tr>
                        <Th>USER ID</Th>
                        <Th>ADD</Th>
                        <Th>Remove</Th>
                    </Tr>
                </Thead>
                <Tbody>
                    {myArray1.map((item) => (
                        <Tr>
                            <Td>{item.customer_id}</Td>
                            <Td>
                                <Button colorScheme={"teal"} fontSize="xl"
                                    onClick={() => handleSubmit(item.customer_id)}
                                >
                                    Confirm Request
                                </Button>
                            </Td>
                            <Td>
                                <Button colorScheme={"red"} fontSize="xl"
                                    onClick={() => handleSubmit1(item.customer_id)}
                                >
                                    Remove Request
                                </Button>
                            </Td>
                        </Tr>
                    ))}
                </Tbody>
            </Table>
        </TableContainer>
        </Container>
    )
}

const NAV_ITEMS = [
    {
        label: 'Dashboard',
        href: '/admin',
    },
    {
        label: 'Modify Employees',
        children: [
            {
                label: 'Add New Employees',
                subLabel: 'Grant employee privilege to users.',
                href: '/addemployees',
            },
            {
                label: 'Remove Employees',
                subLabel: 'Remove employee privilege.',
                href: '/removeemployees',
            },
        ],
    },
    {
        label: 'User Details',
        href: '/getuserinfo',
    },
];

export default AddEmployees