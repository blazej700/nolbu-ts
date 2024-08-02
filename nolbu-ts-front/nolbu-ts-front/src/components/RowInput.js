import React from "react";
import { TextInput } from "react95";
import styled from "styled-components";
import { InputMask } from "@react-input/mask";

const Wrapper = styled.div`
  background: ${({ theme }) => theme.material};

  display: grid;
  grid-template-columns: 25% 75%;
  & > * {
    margin-bottom: 1rem;
  }
`;

let getRowInputType = (rowInputType, register, registerName, inputRef) => {
  if (rowInputType === "number") {
    return (
      <InputMask
        mask="____"
        replacement={{ _: /\d/ }}
        component={TextInput}
        InputMask={inputRef}
        className="input"
        {...register(registerName)}
      />
    );
  } else {
    return <TextInput className="input" {...register(registerName)} />;
  }
};

export default function RowInput({
  labelValue,
  rowInputType,
  register,
  registerName,
  inputRef,
}) {
  return (
    <Wrapper>
      <span>{labelValue}:</span>
      {getRowInputType(rowInputType, register, registerName, inputRef)}
    </Wrapper>
  );
}
