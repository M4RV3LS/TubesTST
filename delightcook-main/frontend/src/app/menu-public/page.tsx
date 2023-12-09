'use client'

import { ChakraProvider, Heading, Image, Spacer } from "@chakra-ui/react";
import Navbar from "@/components/Navbar";
import '@fontsource/cinzel';
import CardWrapper from "@/components/CardWrapper";
import { Card, CardProps } from "@/components/Card";
import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Menu(){
  const [menu_items, set_menu_items] = useState([]);

  useEffect(() => {
    const fetchData =async () => {
      try{
        const menu_items_response = await axios.get('http://127.0.0.1:8000/menu_items/');
        set_menu_items(menu_items_response.data);
      } catch (error) {
        console.log('error fetching data: ', error);
      }
    };
    fetchData();
  }, []);

  return(
      <ChakraProvider>
          <Navbar status={false} />
          <Heading
          textAlign={'center'}
          alignItems={'center'}
          m={5}
          fontFamily={'cinzel'}
          color={'#134074'}>
              Explore All Menus
          </Heading>
          <Spacer></Spacer>
          <CardWrapper columns={{base: 1, sm: 1, md: 2, lg: 3}}>
              {menu_items &&
              menu_items.map((data: any) => (
                <Card
                key={data.menu_id}
                menu_items={[data]}
                status={false}
                detail={false}/>
              ))}
          </CardWrapper>
      </ChakraProvider>
  )
}